# data_fetcher.py

import os
import time
import json
import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from alpha_vantage.timeseries import TimeSeries
from bs4 import BeautifulSoup

# Constants and API keys (user must set these in environment variables for security)
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

# Helper functions for normalization
def normalize_stock_data(df):
    """
    Normalize stock data columns and format datetime
    """
    df = df.rename(columns=lambda x: x.lower())
    if 'date' not in df.columns:
        if 'datetime' in df.columns:
            df.rename(columns={'datetime': 'date'}, inplace=True)
        elif 'timestamp' in df.columns:
            df.rename(columns={'timestamp': 'date'}, inplace=True)
    # Convert date to datetime if not already
    df['date'] = pd.to_datetime(df['date'])
    # Ensure numeric columns
    num_cols = ['open', 'high', 'low', 'close', 'adj close', 'volume']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def normalize_crypto_data(df):
    """
    Normalize crypto data columns and format datetime
    """
    df = df.rename(columns=lambda x: x.lower())
    if 'date' not in df.columns:
        if 'time' in df.columns:
            df.rename(columns={'time': 'date'}, inplace=True)
        elif 'timestamp' in df.columns:
            df.rename(columns={'timestamp': 'date'}, inplace=True)
    # Convert to datetime
    df['date'] = pd.to_datetime(df['date'], unit='ms', errors='coerce')
    # Rename price and volume columns if necessary
    if 'price' in df.columns:
        df.rename(columns={'price': 'close'}, inplace=True)
    if 'volume' not in df.columns and 'vol' in df.columns:
        df.rename(columns={'vol': 'volume'}, inplace=True)
    # Numeric casting
    for col in ['open', 'high', 'low', 'close', 'volume']:
        if col in df.columns:
            df[col] = pd
