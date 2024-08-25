import os
from glob import glob
import numpy as np
import joblib
import pandas as pd
from arch import arch_model
from config import settings
from data import AlphaVantageAPI, SQLRepository


class GarchModel:

    def __init__(self, ticker, repo, use_new_data):
    
        self.ticker = ticker
        self.repo = repo
        self.use_new_data = use_new_data
        self.model_directory = settings.model_directory

    def wrangle_data(self, n_observations):
        # Add new data to database if required
        if self.use_new_data:
        
            api = AlphaVantageAPI()
            df = api.get_daily(ticker=self.ticker)
            
            self.repo.insert_table(table_name=self.ticker, records=df, if_exists='replace')

        # Pull data from SQL database
        df = self.repo.read_table(table_name=self.ticker, limit=n_observations+1)

        # Clean data, attach to class as `data` attribute
        df.sort_index(ascending=True, inplace=True)
        df['return'] = df['close'].pct_change() * 100
        self.data = df['return'].dropna()

    def fit(self, p, q):
        # Train Model, attach to `self.model`
        self.model = arch_model(self.data, p=p, q=q, rescale=False).fit(disp=0)
        self.aic = self.model.aic
        self.bic = self.model.bic

    def __clean_prediction(self, prediction):

        # Calculate forecast start date
        start = prediction.index[0]+pd.DateOffset(days=1)

        # Create date range
        prediction_dates = pd.bdate_range(start=start, periods = prediction.shape[1])

        # Create prediction index labels, ISO 8601 format
        prediction_index = [date.isoformat() for date in prediction_dates]                                 

        # Extract predictions from DataFrame, get square root
        data = np.sqrt(prediction.values.flatten())

        # Combine `data` and `prediction_index` into Series
        prediction_formatted = pd.Series(data, index=prediction_index)

        # Return Series as dictionary
        return prediction_formatted.to_dict()

    def predict_volatility(self, horizon):

        # Generate variance forecast from `self.model`
        prediction = self.model.forecast(horizon=horizon, reindex=False).variance

        # Format prediction with `self.__clean_predction`
        prediction_formatted = self.__clean_prediction(prediction)

        # Return `prediction_formatted`
        return prediction_formatted

    def dump(self):

        # Create timestamp in ISO format
        timestamp = pd.Timestamp.now().isoformat()
        
        # Create filepath, including `self.model_directory`
        filepath = os.path.join(self.model_directory, f"{timestamp}_{self.ticker}.pkl")
        
        # Save `self.model`
        joblib.dump(self.model, filepath)
        
        # Return filepath
        return filepath

    def load(self):

        # Create pattern for glob search
        pattern = os.path.join(self.model_directory, f"*{self.ticker}.pkl")
        # Use glob to get most recent model, handle errors
        try:
            model_path = sorted(glob(pattern))[-1]
        except IndexError:
            raise Exception(f"No model trained for {self.ticker}")
        
        # Load model and attach to `self.model`
        self.model = joblib.load(model_path)