"""
Configuration settings for India Market Dashboard
"""

import os
from dotenv import load_dotenv

load_dotenv()

# App Configuration
APP_TITLE = "India Market Dashboard"
APP_ICON = "📊"
LAYOUT = "wide"

# Data Sources
NIFTY_TICKER = "^NSEI"  # Nifty 50
SENSEX_TICKER = "^BSESN"  # Sensex
RUPEE_TICKER = "USDINR=X"  # USD/INR

# Historical Data Period
DATA_PERIOD = "5y"  # 5 years of historical data
DATA_INTERVAL = "1d"  # Daily data

# Signal Thresholds
PE_RATIO_UNDERVALUED = 18  # Below this = Undervalued
PE_RATIO_OVERVALUED = 25   # Above this = Overvalued

MARKET_CAP_TO_GDP_LOW = 0.8   # Below = Bullish
MARKET_CAP_TO_GDP_HIGH = 1.2  # Above = Bearish

# Moving Averages
SMA_FAST = 50   # 50-day moving average
SMA_SLOW = 200  # 200-day moving average

# RSI Thresholds
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# Cache Settings
CACHE_EXPIRY_HOURS = 24
CACHE_DIR = "data/cache"

# Colors for Signals
COLOR_BULLISH = "#00D084"  # Green
COLOR_BEARISH = "#FF4757"  # Red
COLOR_NEUTRAL = "#FFA502"  # Orange

# Economic Data Thresholds
GDP_GROWTH_GOOD = 5.0      # % (good growth)
INFLATION_GOOD = 4.0       # % (acceptable range)
INFLATION_HIGH = 6.0       # % (high inflation)

# Default Chart Settings
CHART_HEIGHT = 500
CHART_WIDTH = 1000
