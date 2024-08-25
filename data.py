import sqlite3
import pandas as pd
import requests
from config import settings


class AlphaVantageAPI:
    def __init__(self, api_key=settings.alpha_api_key):
        self.__api_key = api_key
    
    def get_daily(self, ticker, output_size='full'):
        url = ("https://www.alphavantage.co/query?"
               "function=TIME_SERIES_DAILY&"
               f"symbol={ticker}&"
               f"outputsize={output_size}&"
               f"datatype=json&"
               f"apikey={self.__api_key}")

        response = requests.get(url=url)

        if "Time Series (Daily)" not in response.json().keys():
            raise Exception(f"Invalid APIs call Please check that symbol {ticker} is collect.")

        # Clean results
        stock_data = response.json()["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(stock_data, orient='index', dtype=float)
        
        # set date to datetime format and set index name
        df.index = pd.to_datetime(df.index)
        df.index.name = "date"
        
        # set columns name
        df.columns = [col.split(". ")[1] for col in df.columns]

        # Return results
        return df


class SQLRepository:
    
    def __init__(self, connection):
        self.connection = connection
    
    def insert_table(self, table_name, records, if_exists='fail'):
        n_inserted = records.to_sql(name=table_name, con=self.connection, if_exists=if_exists)
        
        return {"transaction_successful" : True, "records_inserted" : n_inserted}

    def read_table(self, table_name, limit = None):
        if limit:
            sql = f"SELECT * FROM '{table_name}' limit {limit}"
        else:
            sql = f"SELECT * FROM '{table_name}'"

        df = pd.read_sql(sql=sql, con=self.connection, parse_dates=['date'], index_col='date')

        return df
