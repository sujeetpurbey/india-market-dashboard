"""
Data Fetcher - Fetch market and economic data from various sources
"""

import yfinance as yf
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from config.settings import (
    NIFTY_TICKER, SENSEX_TICKER, RUPEE_TICKER,
    DATA_PERIOD, DATA_INTERVAL, CACHE_EXPIRY_HOURS
)

class DataFetcher:
    """Fetch market data from yfinance and other sources"""
    
    def __init__(self):
        self.nifty_data = None
        self.sensex_data = None
        self.rupee_data = None
        self.vix_data = None
        self.smallcap_data = None
        self.midcap_data = None
        self.cache = {}
        self.live_cache = {} # New cache specifically for real-time prices
    
    def _is_cache_valid(self, key, is_live=False):
        """Check if cache is still valid. Live cache expires in 60 seconds."""
        cache_dict = self.live_cache if is_live else self.cache
        
        if key not in cache_dict:
            return False
            
        cached_time = cache_dict[key]['time']
        
        if is_live:
            # Real-time data expires in 60 seconds
            age_seconds = (datetime.now() - cached_time).total_seconds()
            return age_seconds < 60
        else:
            # Historical data uses the settings.py expiry
            age_hours = (datetime.now() - cached_time).total_seconds() / 3600
            return age_hours < CACHE_EXPIRY_HOURS
    
    def _get_from_cache(self, key, is_live=False):
        """Get data from cache"""
        cache_dict = self.live_cache if is_live else self.cache
        if self._is_cache_valid(key, is_live):
            return cache_dict[key]['data']
        return None
    
    def _set_cache(self, key, data, is_live=False):
        """Store data in cache"""
        cache_dict = self.live_cache if is_live else self.cache
        cache_dict[key] = {
            'data': data,
            'time': datetime.now()
        }
    
    def _generate_demo_data(self, ticker, base_price=None):
        """Generate realistic demo data when live data is unavailable"""
        print(f"Generating demo data for {ticker}...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        if ticker == "^NSEI": base_price = 19500
        elif ticker == "^BSESN": base_price = 64500
        elif ticker == "USDINR=X": base_price = 82.5
        elif ticker == "^INDIAVIX": base_price = 15.0
        elif ticker == "^NSMIDCAP": base_price = 18000
        elif ticker == "^NSMALLCAP": base_price = 12000
        elif base_price is None: base_price = 10000
        
        returns = np.random.normal(0.0005, 0.015, len(dates))
        prices = base_price * np.exp(np.cumsum(returns))
        
        df = pd.DataFrame({
            'Open': prices * (1 + np.random.uniform(-0.01, 0.01, len(prices))),
            'High': prices * (1 + np.random.uniform(0, 0.02, len(prices))),
            'Low': prices * (1 + np.random.uniform(-0.02, 0, len(prices))),
            'Close': prices,
            'Volume': np.random.randint(1000000, 100000000, len(prices))
        }, index=dates)
        return df
    
    def _fetch_historical_data(self, ticker, name, attr_name):
        """Generic method to fetch historical data to avoid repeating code"""
        try:
            cached = self._get_from_cache(name)
            if cached is not None:
                setattr(self, attr_name, cached)
                return cached
            
            print(f"📥 Fetching {name} historical data...")
            data = yf.download(
                ticker, period=DATA_PERIOD, interval=DATA_INTERVAL,
                progress=False, auto_adjust=True, timeout=10
            )
            
            if data is None or len(data) == 0:
                raise Exception("Empty data received")
                
            self._set_cache(name, data)
            setattr(self, attr_name, data)
            return data
            
        except Exception as e:
            print(f"⚠️ Could not fetch {name}: {e}. Using demo data.")
            demo_data = self._generate_demo_data(ticker)
            self._set_cache(name, demo_data)
            setattr(self, attr_name, demo_data)
            return demo_data

    def fetch_nifty_data(self): return self._fetch_historical_data(NIFTY_TICKER, 'nifty', 'nifty_data')
    def fetch_sensex_data(self): return self._fetch_historical_data(SENSEX_TICKER, 'sensex', 'sensex_data')
    def fetch_rupee_data(self): return self._fetch_historical_data(RUPEE_TICKER, 'rupee', 'rupee_data')
    def fetch_vix_data(self): return self._fetch_historical_data("^INDIAVIX", 'vix', 'vix_data')
    def fetch_midcap_data(self): return self._fetch_historical_data("^NSMIDCAP", 'midcap', 'midcap_data')
    def fetch_smallcap_data(self): return self._fetch_historical_data("^NSMALLCAP", 'smallcap', 'smallcap_data')
    
    def get_latest_price(self, ticker):
        """Get near real-time price using 1-minute intervals and a 60-second cache."""
        try:
            cache_key = f"live_price_{ticker}"
            cached = self._get_from_cache(cache_key, is_live=True)
            if cached is not None:
                return cached
            
            # Use interval="1m" to get the absolute latest intraday tick
            data = yf.download(ticker, period="1d", interval="1m", progress=False, auto_adjust=True, timeout=5)
            if len(data) > 0:
                price = float(data['Close'].iloc[-1]) # Ensure it's a clean float
                self._set_cache(cache_key, price, is_live=True)
                return price
            return None
        except Exception as e:
            print(f"⚠️ Error fetching live price for {ticker}: {e}")
            return None
    
    def get_price_change(self, ticker, period_days=1):
        """Get percentage change for a ticker"""
        try:
            cache_key = f"live_change_{ticker}_{period_days}d"
            cached = self._get_from_cache(cache_key, is_live=True)
            if cached is not None:
                return cached
            
            data = yf.download(
                ticker, period=f"{period_days+1}d", progress=False, auto_adjust=True, timeout=5
            )
            if len(data) >= 2:
                old_price = float(data['Close'].iloc[0])
                new_price = float(data['Close'].iloc[-1])
                change_pct = ((new_price - old_price) / old_price) * 100
                self._set_cache(cache_key, change_pct, is_live=True)
                return change_pct
            return None
        except Exception as e:
            print(f"⚠️ Error calculating price change: {e}")
            return None
    
    def fetch_all_data(self):
        """Fetch all market data efficiently"""
        self.fetch_nifty_data()
        self.fetch_sensex_data()
        self.fetch_rupee_data()
        self.fetch_vix_data()
        self.fetch_midcap_data()
        self.fetch_smallcap_data()
        
        return {
            'nifty': self.nifty_data,
            'sensex': self.sensex_data,
            'rupee': self.rupee_data,
            'vix': self.vix_data,
            'midcap': self.midcap_data,
            'smallcap': self.smallcap_data
        }
