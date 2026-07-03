# Data Sources Documentation

## Market Data

### Nifty 50 & Sensex
**Source**: Yahoo Finance (via yfinance)
**Ticker**: ^NSEI (Nifty 50), ^BSESN (Sensex)
**Frequency**: Daily
**Data**: Open, High, Low, Close, Volume
**Cost**: Free
**Update**: End of trading day

**yfinance Code**:
```python
import yfinance as yf
nifty = yf.download("^NSEI", period="5y")
```

### USD/INR Exchange Rate
**Source**: Yahoo Finance
**Ticker**: USDINR=X
**Frequency**: Daily
**Cost**: Free

## Economic Data

### RBI Data (Reserve Bank of India)
**Website**: https://www.rbi.org.in/
**Data Available**:
- Repo Rate
- Reverse Repo Rate
- CRR (Cash Reserve Ratio)
- Monetary Policy Decisions

**Format**: PDF reports, CSV downloads
**Frequency**: Monthly/Quarterly
**Cost**: Free

### Inflation Data (CPI)
**Source**: Ministry of Statistics, Government of India
**Website**: https://pib.gov.in/
**Frequency**: Monthly
**Data**: Consumer Price Index (CPI)
**Cost**: Free

### GDP Data
**Source**: National Statistical Office (NSO)
**Website**: https://mospi.gov.in/
**Frequency**: Quarterly
**Data**: GDP growth rate, Sector-wise growth
**Cost**: Free

### IIP (Industrial Production)
**Source**: NSO
**Frequency**: Monthly (provisional), later revised
**Cost**: Free

## Alternative Data Sources

### Trading Economics
**Website**: https://tradingeconomics.com/
**Coverage**: Indian and global economic indicators
**API**: Available (freemium)
**Data**: Inflation, unemployment, interest rates, etc.

### World Bank
**Website**: https://data.worldbank.org/
**Data**: Long-term economic data
**Format**: API, CSV
**Coverage**: Global
**Cost**: Free

### Finnhub
**Website**: https://finnhub.io/
**API**: REST API
**Features**: Stock data, news, economic calendar
**Cost**: Free tier available

## Data Quality & Verification

1. **Cross-validate** data from multiple sources
2. **Check timestamps** for consistency
3. **Verify outliers** before using in calculations
4. **Handle missing data** appropriately
5. **Test API connections** regularly

## API Integration Examples

### yfinance
```python
import yfinance as yf

# Download historical data
data = yf.download("^NSEI", start="2020-01-01", end="2024-01-01")

# Get ticker info
ticker = yf.Ticker("^NSEI")
info = ticker.info
```

### Requests Library (for web scraping)
```python
import requests
from bs4 import BeautifulSoup

url = "https://example.com/data"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
```

## Data Storage Strategy

- **CSV Files**: Historical data (daily backups)
- **JSON Cache**: Recent data for fast access
- **Database**: Future implementation for large-scale storage

## Data Update Schedule

| Data Type | Frequency | Update Time |
|-----------|-----------|-------------|
| Stock Prices | Daily | 3:30 PM IST |
| Inflation (CPI) | Monthly | Usually 2nd week |
| GDP | Quarterly | 2 months after quarter |
| RBI Repo Rate | As announced | Varies |
| IIP | Monthly | Around 12th of month |

## Troubleshooting

### Data Not Available
- Check internet connection
- Verify API status pages
- Check if ticker symbols are correct
- Look for rate limiting issues

### Stale Data
- Check last update timestamp
- Verify cache expiry settings
- Manually refresh if needed

### API Rate Limits
- Implement retry logic with backoff
- Cache data aggressively
- Use multiple data sources
