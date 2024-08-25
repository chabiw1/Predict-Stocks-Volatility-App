import streamlit as st
import requests
import os
from datetime import datetime, date
import matplotlib.pyplot as plt
import pandas as pd

### Title ###
st.title("Volatility Forecasting App")
st.subheader("ARCH(1,1)")
st.markdown("""For accurate forecasting, it is recommended to have a training dataset that is at least 6 to 12 times the number of days you wish to forecast. For example, if you want to forecast the next 30 days, you should ideally train your model with data covering at least 6 to 12 months.
""")

### Training Layer ####
st.subheader("Train New Model")
ticker_train = st.text_input("Training Stock")


start_date = st.date_input("Training Start Date:", 
                           min_value=date(2015, 1, 1),
                           max_value=datetime.now().date()
                           )
end_date = datetime.now().date()

training_days = end_date - start_date

if st.button("Train Model"):
    # Call the API to train the model
    response = requests.post(
        "http://localhost:8008/fit",  
        json={"ticker": ticker_train, 
              "use_new_data": True,
              "n_observations": training_days.days,
              "p": 1,
              "q": 1
              }
    )
    if response.status_code == 200:
        st.success("Model trained successfully!")
    else:
        st.error("Error in training model.")

### Prediction Layer ###
st.subheader("Predict Volatility")
st.markdown("Remark : Predict by latest model of selected ticker")

ticker_predict = st.text_input("Stock")
forcast_days = st.number_input("Number of Days You Want to Forcast",min_value=1,value=1,step=1)

if st.button("Predict Volatility"):
    # Call the API to predict volatility
    response = requests.post(
        "http://localhost:8008/predict",
        json={"ticker": ticker_predict, "n_days": forcast_days}  
    )
    if response.status_code == 200:
        prediction = response.json()
        st.write("Prediction Results:")
        st.json(prediction)
        
        if "forecast" in prediction:
            
            forecast = prediction["forecast"]
            forecast_df = pd.DataFrame(list(forecast.items()), columns=['Date', 'Volatility'])
            forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])
            forecast_df.set_index('Date', inplace=True)

            # Plotting
            plt.figure(figsize=(12, 6))
            plt.plot(forecast_df.index, forecast_df['Volatility'], marker='o', linestyle='-', color='blue')
            plt.title('Forecasted Volatility')
            plt.xlabel('Date')
            plt.ylabel('Volatility')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Display in Streamlit
            st.pyplot(plt)
        else:
            st.error("Forecast data not found in the response.")

    else:
        st.error("Error in API call.")


