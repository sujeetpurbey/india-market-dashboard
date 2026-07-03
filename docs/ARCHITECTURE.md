# India Market Dashboard - Architecture

## Overview

The India Market Dashboard is a Python-based Streamlit application that tracks Indian economic indicators and provides market entry/exit signals.

## System Components

### 1. Data Layer (`src/data_fetcher.py`)

**Responsibility**: Fetch market and economic data from external sources

**Key Functions**:
- `DataFetcher.fetch_nifty_data()` - Get Nifty 50 historical data
- `DataFetcher.fetch_sensex_data()` - Get Sensex data
- `DataFetcher.fetch_rupee_data()` - Get USD/INR exchange rates
- `DataFetcher.get_latest_price()` - Get current price for any ticker
- `DataFetcher.get_price_change()` - Calculate percentage change

**Data Sources**:
- yfinance API for stock market data
- RSS feeds for economic news
- Web scraping for additional data

### 2. Indicators Layer (`src/indicators.py`)

**Responsibility**: Calculate technical and fundamental indicators

**Key Indicators**:
- **Technical**: SMA, RSI, MACD, Bollinger Bands, ATR
- **Fundamental**: P/E Ratio, Market Cap to GDP, Dividend Yield

**Algorithm Examples**:
- RSI: Relative Strength Index for overbought/oversold conditions
- MACD: Momentum indicator for trend changes
- Moving Averages: Golden/Death Crosses for entry/exit

### 3. Signal Analysis Layer (`src/signals.py`)

**Responsibility**: Generate trading signals based on indicators

**Signal Generation**:
1. Calculate bullish and bearish scores
2. Analyze valuation metrics
3. Analyze technical indicators
4. Analyze macro indicators
5. Generate final signal: BUY/SELL/HOLD

**Scoring System**:
- Each indicator contributes to bullish or bearish score
- Final signal is determined by net score
- Signal strength is calculated as bullish % of total

### 4. Visualization Layer (`src/visualizations.py`)

**Responsibility**: Create charts and visual components

**Components**:
- Price charts with moving averages
- Gauge charts for signal strength
- Indicator tables
- Market metrics cards

### 5. Presentation Layer (`src/main.py`)

**Responsibility**: Streamlit UI and dashboard layout

**Features**:
- Multi-tab interface
- Real-time data refresh
- Signal visualization
- Settings panel

## Data Flow

```
┌─────────────────────┐
│  External Data      │
│  Sources            │
│  (yfinance, RBI)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  DataFetcher        │ (src/data_fetcher.py)
│  Fetch & Parse      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Indicators         │ (src/indicators.py)
│  Calculate Metrics  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  SignalAnalyzer     │ (src/signals.py)
│  Generate Signals   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Visualizations     │ (src/visualizations.py)
│  Create Charts      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Streamlit App      │ (src/main.py)
│  Display Dashboard  │
└─────────────────────┘
```

## Configuration

All settings are centralized in `config/settings.py`:
- Tickers and symbols
- Technical indicator periods
- Signal thresholds
- UI preferences

## Caching Strategy

- Market data cached for 24 hours
- Economic data cached for 7 days
- Cache stored in `data/cache/` directory
- Automatic expiry check before use

## Future Enhancements

1. **Real-time Alerts**: WebSocket connections for live updates
2. **Backtesting**: Historical strategy testing
3. **Portfolio Tracking**: User portfolio management
4. **Machine Learning**: Predictive models for better signals
5. **Mobile App**: React Native mobile version
6. **Multi-user**: User accounts and personalization

## Performance Considerations

- Lazy loading of heavy components
- Data caching to reduce API calls
- Efficient pandas operations for large datasets
- Streamlit session state for state management
