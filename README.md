# Predict-Stocks-Volatility-App

Welcome to the Volatility Prediction Project! This project aims to create a robust system for forecasting stock market volatility, a critical component for financial analysis and decision-making. By leveraging advanced statistical models and modern technologies, this project helps investors assess risk and make informed trading decisions.

[App](https://github.com/user-attachments/assets/99a21bc4-380e-4fbf-ae61-c31117bbac48)



Before diving into the core components, it's essential to understand the configuration module that manages key settings such as API keys and database paths, ensuring that the system operates smoothly across different environments.

## Configuration (`config.py`)

To ensure seamless operation across different environments, the project uses a configuration file to manage essential settings, such as API keys and database paths. The `config.py` module extracts these settings from a `.env` file, making it easy to adjust configurations without modifying the core code.

- **`Settings` Class:**
  - **Function:** Utilizes Pydantic to define and validate configuration settings, ensuring that all necessary information is correctly set up before the application runs.
  - **Key Attributes:**
    - `alpha_api_key`: API key for AlphaVantage, used to access market data.
    - `db_name`: Path to the SQLite database where stock data is stored.
    - `model_directory`: Directory path for saving and loading machine learning models.

- **Functions:**
  - `return_full_path(filename: str = ".env")`: Returns the absolute path of the `.env` file, ensuring that the configuration settings are correctly located.
  - **Instance:** `settings` provides access to configuration settings throughout the project, streamlining access to critical parameters.

**Workflow:**
- Reads configuration settings from the `.env` file, providing necessary information for API access and database interactions. This separation of configuration from code ensures that sensitive information like API keys is kept secure and that configuration changes can be made easily.


```
import os
from pydantic import BaseSettings

def return_full_path(filename: str = ".env") -> str:
   
    absolute_path = os.path.abspath(__file__)
    directory_name = os.path.dirname(absolute_path)
    full_path = os.path.join(directory_name, filename)
    return full_path

class Settings(BaseSettings):
  
    alpha_api_key: str
    db_name: str
    model_directory: str
    class Config:
        env_file = return_full_path(".env")
settings = Settings()
```
## Purpose

The goal of this project is to develop a system for predicting stock market volatility, an essential aspect of financial analysis that helps investors assess risk and make informed decisions. The project leverages the **Generalized Autoregressive Conditional Heteroskedasticity (GARCH)** model, particularly the **GARCH(1,1)** variant, which is ideal for time series data characterized by volatility clustering, such as stock prices.

## Components and Workflow

The project is divided into four main components:

1. **Data Handling (`data.py`)**
2. **Model Implementation (`model.py`)**
3. **API Implementation (`main.py`)**
4. **User Interface (`app.py`)**
   
![Predict Volatility Diagram](https://github.com/user-attachments/assets/e9ec7435-88c3-437c-8950-8151cac086af)

### 1. Data Handling (`data.py`)

**Purpose:** Manage data retrieval and storage.

- **`AlphaVantageAPI` Class:**
  - **Function:** Retrieves historical stock data from AlphaVantage.
  - **Key Method:** 
    - `get_daily(ticker, output_size='full')`: Fetches daily stock prices and returns them as a DataFrame.
  - **AlphaVantage:** A service providing historical and real-time market data, essential for training and forecasting stock volatility.

- **`SQLRepository` Class:**
  - **Function:** Handles database operations.
  - **Key Methods:** 
    - `insert_table(table_name, records, if_exists='fail')`: Inserts data into the database.
    - `read_table(table_name, limit=None)`: Reads data from the database.

**Workflow:**
- Fetches stock data using `AlphaVantageAPI`.
- Manages storage and retrieval of data using `SQLRepository`.

### 2. Model Implementation (`model.py`)

**Purpose:** Implement the GARCH model for forecasting volatility.

- **`GarchModel` Class:**
  - **Function:** Uses the GARCH model to forecast volatility.
  - **Key Methods:**
    - `wrangle_data(n_observations)`: Prepares data for the model.
    - `fit(p, q)`: Fits the GARCH model with specified parameters.
    - `predict_volatility(horizon)`: Predicts future volatility.
    - `dump()`: Saves the trained model.
    - `load()`: Loads a saved model.

**Workflow:**
- Prepares data, trains the model, and generates forecasts with `GarchModel`.

### 3. API Implementation (`main.py`)

**Purpose:** Provide endpoints for model training and predictions.

- **`FastAPI` Application:**
  - **Endpoints:**
    - `/fit`: Trains the GARCH model.
    - `/predict`: Provides volatility forecasts.

- **Key Functions:**
  - `fit_model(request: FitIn)`: Trains the model and returns metrics like AIC and BIC.
  - `get_prediction(request: PredictIn)`: Returns volatility forecasts based on the latest model.

**Workflow:**
- Handles API requests for training and prediction, interacting with `GarchModel`.

### 4. User Interface (`app.py`)

**Purpose:** Provide an interactive interface for users.

- **Streamlit Application:**
  - **Training Interface:** 
    - Inputs: Stock ticker, start date, end date.
    - Function: Trains a new model and displays status messages.
  
  - **Prediction Interface:**
    - Inputs: Stock ticker, number of forecast days.
    - Function: Predicts volatility and visualizes results.

**Workflow:**
- Users interact with the model through the Streamlit app, which communicates with the FastAPI backend for training and predictions, and displays forecast results in graphs.

## Summary

This project integrates several components to provide a complete solution for stock market volatility prediction:

- **Data Handling:** Fetches and stores stock data using **AlphaVantage**, a service that provides historical and real-time market data essential for training and forecasting.
- **Model Implementation:** Utilizes the **Generalized Autoregressive Conditional Heteroskedasticity (GARCH)** model, specifically the **GARCH(1,1)** variant. This model effectively captures volatility clustering in financial time series data by using one lag for both the autoregressive and moving average components.
- **API Implementation:** Exposes functionalities for training and prediction through a FastAPI application.
- **User Interface:** Allows users to interact with the model and visualize results through a Streamlit app.
- **Configuration:** Manages project settings and credentials.

By combining these elements, the project delivers a robust tool for forecasting stock volatility, providing valuable insights for investors and financial analysts.
