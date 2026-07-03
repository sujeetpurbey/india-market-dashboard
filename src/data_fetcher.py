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
        self.cache = {}
    
    def _is_cache_valid(self, key):
        """Check if cache is still valid"""
        if key not in self.cache:
            return False
        
        cached_time = self.cache[key]['time']
        age_hours = (datetime.now() - cached_time).total_seconds() / 3600
        return age_hours < CACHE_EXPIRY_HOURS
    
    def _get_from_cache(self, key):
        """Get data from cache"""
        if self._is_cache_valid(key):
            return self.cache[key]['data']
        return None
    
    def _set_cache(self, key, data):
        """Store data in cache"""
        self.cache[key] = {
            'data': data,
            'time': datetime.now()
        }
    
    def _generate_demo_data(self, ticker):
        """Generate realistic demo data when live data is unavailable"""
        print(f"Generating demo data for {ticker}...")
        
        # Create date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate realistic price data
        if ticker == NIFTY_TICKER:
            base_price = 19500
            company_name = "Nifty 50"
        elif ticker == SENSEX_TICKER:
            base_price = 64500
            company_name = "Sensex"
        else:  # USD/INR
            base_price = 82.5
            company_name = "USD/INR"
        
        # Generate price with random walk
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
    
    def fetch_nifty_data(self):
        """Fetch Nifty 50 historical data"""
        try:
            # Check cache first
            cached = self._get_from_cache('nifty')
            if cached is not None:
                print("✅ Using cached Nifty 50 data")
                self.nifty_data = cached
                return self.nifty_data
            
            print("📥 Fetching Nifty 50 data from yfinance...")
            try:
                self.nifty_data = yf.download(
                    NIFTY_TICKER,
                    period=DATA_PERIOD,
                    interval=DATA_INTERVAL,
                    progress=False,
                    auto_adjust=True,
                    timeout=10
                )
                
                if self.nifty_data is None or len(self.nifty_data) == 0:
                    raise Exception("Empty data received from yfinance")
                
                # Cache it
                self._set_cache('nifty', self.nifty_data)
                print("✅ Nifty 50 data fetched successfully")
                
            except Exception as e:
                print(f"⚠️ Could not fetch from yfinance: {e}")
                print("📊 Using demo data instead...")
                self.nifty_data = self._generate_demo_data(NIFTY_TICKER)
                self._set_cache('nifty', self.nifty_data)
            
            # Add delay to avoid rate limiting
            time.sleep(2)
            
            return self.nifty_data
        except Exception as e:
            print(f"❌ Error in fetch_nifty_data: {e}")
            return None
    
    def fetch_sensex_data(self):
        """Fetch Sensex historical data"""
        try:
            # Check cache first
            cached = self._get_from_cache('sensex')
            if cached is not None:
                print("✅ Using cached Sensex data")
                self.sensex_data = cached
                return self.sensex_data
            
            print("📥 Fetching Sensex data from yfinance...")
            try:
                self.sensex_data = yf.download(
                    SENSEX_TICKER,
                    period=DATA_PERIOD,
                    interval=DATA_INTERVAL,
                    progress=False,
                    auto_adjust=True,
                    timeout=10
                )
                
                if self.sensex_data is None or len(self.sensex_data) == 0:
                    raise Exception("Empty data received from yfinance")
                
                # Cache it
                self._set_cache('sensex', self.sensex_data)
                print("✅ Sensex data fetched successfully")
                
            except Exception as e:
                print(f"⚠️ Could not fetch from yfinance: {e}")
                print("📊 Using demo data instead...")
                self.sensex_data = self._generate_demo_data(SENSEX_TICKER)
                self._set_cache('sensex', self.sensex_data)
            
            # Add delay to avoid rate limiting
            time.sleep(2)
            
            return self.sensex_data
        except Exception as e:
            print(f"❌ Error in fetch_sensex_data: {e}")
            return None
    
    def fetch_rupee_data(self):
        """Fetch USD/INR exchange rate data"""
        try:
            # Check cache first
            cached = self._get_from_cache('rupee')
            if cached is not None:
                print("✅ Using cached Rupee data")
                self.rupee_data = cached
                return self.rupee_data
            
            print("📥 Fetching USD/INR data from yfinance...")
            try:
                self.rupee_data = yf.download(
                    RUPEE_TICKER,
                    period=DATA_PERIOD,
                    interval=DATA_INTERVAL,
                    progress=False,
                    auto_adjust=True,
                    timeout=10
                )
                
                if self.rupee_data is None or len(self.rupee_data) == 0:
                    raise Exception("Empty data received from yfinance")
                
                # Cache it
                self._set_cache('rupee', self.rupee_data)
                print("✅ USD/INR data fetched successfully")
                
            except Exception as e:
                print(f"⚠️ Could not fetch from yfinance: {e}")
                print("📊 Using demo data instead...")
                self.rupee_data = self._generate_demo_data(RUPEE_TICKER)
                self._set_cache('rupee', self.rupee_data)
            
            # Add delay to avoid rate limiting
            time.sleep(2)
            
            return self.rupee_data
        except Exception as e:
            print(f"❌ Error in fetch_rupee_data: {e}")
            return None
    
    def get_latest_price(self, ticker):
        """Get latest price for a ticker"""
        try:
            # Check cache first
            cache_key = f"price_{ticker}"
            cached = self._get_from_cache(cache_key)
            if cached is not None:
                return cached
            
            data = yf.download(ticker, period="1d", progress=False, auto_adjust=True, timeout=10)
            if len(data) > 0:
                price = data['Close'].iloc[-1]
                self._set_cache(cache_key, price)
                time.sleep(2)
                return price
            return None
        except Exception as e:
            print(f"⚠️ Error fetching latest price for {ticker}: {e}")
            return None
    
    def get_price_change(self, ticker, period_days=1):
        """Get percentage change for a ticker"""
        try:
            cache_key = f"change_{ticker}_{period_days}d"
            cached = self._get_from_cache(cache_key)
            if cached is not None:
                return cached
            
            data = yf.download(
                ticker,
                period=f"{period_days+1}d",
                progress=False,
                auto_adjust=True,
                timeout=10
            )
            if len(data) >= 2:
                old_price = data['Close'].iloc[0]
                new_price = data['Close'].iloc[-1]
                change_pct = ((new_price - old_price) / old_price) * 100
                self._set_cache(cache_key, change_pct)
                time.sleep(2)
                return change_pct
            return None
        except Exception as e:
            print(f"⚠️ Error calculating price change: {e}")
            return None
    
    def fetch_all_data(self):
        """Fetch all market data"""
        self.fetch_nifty_data()
        time.sleep(1)
        self.fetch_sensex_data()
        time.sleep(1)
        self.fetch_rupee_data()
        
        return {
            'nifty': self.nifty_data,
            'sensex': self.sensex_data,
            'rupee': self.rupee_data
        }
