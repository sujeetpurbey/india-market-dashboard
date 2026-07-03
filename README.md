# India Market Dashboard 🇮🇳📊

A free, open-source dashboard to track Indian economic indicators, market health, and stock market valuations. Get actionable insights on when to enter or exit the market.

## Features

- **Economic Indicators**: Track inflation, GDP, IIP, RBI rates, rupee trends
- **Market Metrics**: Nifty 50 P/E, Sensex valuation, market breadth
- **Entry/Exit Signals**: Rules-based trading signals based on fundamentals & technicals
- **Real-time Updates**: Daily market data and economic metrics
- **Interactive Dashboard**: Beautiful visualizations with Streamlit

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Sources**: yfinance, NSE scraping, RBI data
- **Deployment**: Streamlit Cloud (Free)

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/sujeetpurbey/india-market-dashboard.git
cd india-market-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run src/main.py
```

The dashboard will open at `http://localhost:8501`

## Project Structure

```
inda-market-dashboard/
├── README.md                    # Project overview
├── requirements.txt             # Python dependencies
├── .gitignore
├── config/
│   └── settings.py             # Configuration & constants
├── src/
│   ├── main.py                 # Streamlit app entry point
│   ├── data_fetcher.py         # Fetch economic data
│   ├── indicators.py           # Calculate market indicators
│   ├── signals.py              # Entry/exit signal logic
│   ├── visualizations.py       # Chart components
│   └── utils.py                # Helper functions
├── data/
│   └── .gitkeep               # Data storage (cached)
├── docs/
│   ├── ARCHITECTURE.md         # System design
│   ├── DATA_SOURCES.md         # Data source documentation
│   └── ROADMAP.md              # Feature roadmap
└── tests/
    └── .gitkeep
```

## Roadmap

### Phase 1: MVP (Week 1-2)
- [ ] Set up Streamlit dashboard structure
- [ ] Fetch Nifty 50 & Sensex data (yfinance)
- [ ] Display basic market metrics (P/E, Market Cap to GDP)
- [ ] Show basic entry/exit signals

### Phase 2: Enhancements (Week 3-4)
- [ ] Integrate RBI economic data
- [ ] Add inflation, GDP, IIP metrics
- [ ] Build signal scoring system
- [ ] Add sector-wise analysis
- [ ] Deploy to Streamlit Cloud

### Phase 3: Advanced (Future)
- [ ] Real-time alerts
- [ ] Historical backtesting
- [ ] Portfolio tracking
- [ ] News sentiment analysis

## Data Sources

- **Stock Data**: yfinance (Yahoo Finance)
- **Nifty/Sensex**: NSE data via yfinance
- **Economic Data**: RBI, World Bank, Trading Economics
- **Macroeconomic**: Indian government statistics

## Entry/Exit Signal Logic

### Entry Signals (Bullish)
- Nifty P/E < Historical average (15-20 range)
- Strong GDP growth (> 5%)
- Low inflation (< 5%)
- Positive momentum indicators

### Exit Signals (Bearish)
- Nifty P/E > 25
- Slowing GDP growth
- High inflation
- Negative breadth indicators

## Installation & Deployment

### Local Development
```bash
pip install -r requirements.txt
streamlit run src/main.py
```

### Deploy to Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect GitHub account
4. Deploy the repository

## Contributing

Feel free to fork, improve, and submit PRs!

## Disclaimer

⚠️ **This is for educational and informational purposes only. Not financial advice. Always consult a financial advisor before making investment decisions.**

## License

MIT License - feel free to use for personal or commercial projects

## Contact

Built by [@sujeetpurbey](https://github.com/sujeetpurbey)

---

**Start building your financial intelligence! 🚀**
