"""
Market Indicators - Calculate various technical and fundamental indicators
"""

import pandas as pd
import numpy as np
from config.settings import (
    SMA_FAST, SMA_SLOW, RSI_OVERBOUGHT, RSI_OVERSOLD
)


class Indicators:
    """Calculate technical and fundamental indicators"""
    
    @staticmethod
    def calculate_sma(data, period):
        """Calculate Simple Moving Average"""
        return data.rolling(window=period).mean()
    
    @staticmethod
    def calculate_rsi(data, period=14):
        """Calculate Relative Strength Index (RSI)"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(data, fast=12, slow=26, signal=9):
        """Calculate MACD (Moving Average Convergence Divergence)"""
        ema_fast = data.ewm(span=fast).mean()
        ema_slow = data.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        macd_hist = macd - macd_signal
        
        return macd, macd_signal, macd_hist
    
    @staticmethod
    def calculate_bollinger_bands(data, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        sma = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return upper_band, sma, lower_band
    
    @staticmethod
    def calculate_atr(high, low, close, period=14):
        """Calculate Average True Range (volatility indicator)"""
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def get_pe_ratio(market_cap, net_profit):
        """Calculate P/E Ratio"""
        if net_profit > 0:
            return market_cap / net_profit
        return None
    
    @staticmethod
    def get_market_cap_to_gdp(market_cap, gdp):
        """Calculate Market Cap to GDP ratio"""
        if gdp > 0:
            return market_cap / gdp
        return None
