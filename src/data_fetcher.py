"""
Data Fetcher - Fetch market and economic data from various sources
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config.settings import (
    NIFTY_TICKER, SENSEX_TICKER, RUPEE_TICKER,
    DATA_PERIOD, DATA_INTERVAL
)


class DataFetcher:
    """Fetch market data from yfinance and other sources"""
    
    def __init__(self):
        self.nifty_data = None
        self.sensex_data = None
        self.rupee_data = None
    
    def fetch_nifty_data(self):
        """Fetch Nifty 50 historical data"""
        try:
            self.nifty_data = yf.download(
                NIFTY_TICKER,
                period=DATA_PERIOD,
                interval=DATA_INTERVAL,
                progress=False
            )
            return self.nifty_data
        except Exception as e:
            print(f"Error fetching Nifty data: {e}")
            return None
    
    def fetch_sensex_data(self):
        """Fetch Sensex historical data"""
        try:
            self.sensex_data = yf.download(
                SENSEX_TICKER,
                period=DATA_PERIOD,
                interval=DATA_INTERVAL,
                progress=False
            )
            return self.sensex_data
        except Exception as e:
            print(f"Error fetching Sensex data: {e}")
            return None
    
    def fetch_rupee_data(self):
        """Fetch USD/INR exchange rate data"""
        try:
            self.rupee_data = yf.download(
                RUPEE_TICKER,
                period=DATA_PERIOD,
                interval=DATA_INTERVAL,
                progress=False
            )
            return self.rupee_data
        except Exception as e:
            print(f"Error fetching Rupee data: {e}")
            return None
    
    def get_latest_price(self, ticker):
        """Get latest price for a ticker"""
        try:
            data = yf.download(ticker, period="1d", progress=False)
            return data['Close'].iloc[-1]
        except Exception as e:
            print(f"Error fetching latest price for {ticker}: {e}")
            return None
    
    def get_price_change(self, ticker, period_days=1):
        """Get percentage change for a ticker"""
        try:
            data = yf.download(
                ticker,
                period=f"{period_days+1}d",
                progress=False
            )
            if len(data) >= 2:
                old_price = data['Close'].iloc[0]
                new_price = data['Close'].iloc[-1]
                change_pct = ((new_price - old_price) / old_price) * 100
                return change_pct
            return None
        except Exception as e:
            print(f"Error calculating price change: {e}")
            return None
    
    def fetch_all_data(self):
        """Fetch all market data"""
        self.fetch_nifty_data()
        self.fetch_sensex_data()
        self.fetch_rupee_data()
        return {
            'nifty': self.nifty_data,
            'sensex': self.sensex_data,
            'rupee': self.rupee_data
        }
