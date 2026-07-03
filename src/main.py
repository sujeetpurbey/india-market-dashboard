"""
Main Streamlit app for India Market Dashboard
"""

import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from config.settings import APP_TITLE, APP_ICON, LAYOUT
from data_fetcher import DataFetcher
from visualizations import create_market_metrics, create_signal_gauge
from signals import SignalAnalyzer

# Page Configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.markdown("Track Indian economic indicators, market health, and get entry/exit signals")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        refresh_interval = st.selectbox(
            "Refresh Data Every:",
            ["1 hour", "4 hours", "Daily"]
        )
        
        show_technical = st.checkbox("Show Technical Indicators", value=True)
        show_macro = st.checkbox("Show Macro Indicators", value=True)
        show_signals = st.checkbox("Show Entry/Exit Signals", value=True)
    
    # Main Content Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Market Overview", "📊 Indicators", "🎯 Signals", "📖 About"]
    )
    
    with tab1:
        st.header("Market Overview")
        st.info("🔄 Fetching latest market data...")
        
        try:
            fetcher = DataFetcher()
            
            # Market Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Nifty 50", "Coming Soon", "+2.5%")
            
            with col2:
                st.metric("Sensex", "Coming Soon", "+1.8%")
            
            with col3:
                st.metric("USD/INR", "Coming Soon", "-0.2%")
            
            with col4:
                st.metric("VIX (India)", "Coming Soon", "-5%")
            
            st.markdown("---")
            
            # Charts (Placeholder)
            st.subheader("Nifty 50 - 1 Year Performance")
            st.write("Chart will be displayed here")
            
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
    
    with tab2:
        st.header("Economic & Market Indicators")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Market Valuation")
            st.write("- Nifty P/E Ratio")
            st.write("- Market Cap to GDP")
            st.write("- Dividend Yield")
        
        with col2:
            st.subheader("📈 Macro Indicators")
            st.write("- Inflation (CPI)")
            st.write("- GDP Growth Rate")
            st.write("- IIP (Industrial Production)")
    
    with tab3:
        st.header("Entry/Exit Signals")
        
        st.subheader("Overall Market Signal")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.write("🟡 Neutral - Waiting for confirmation")
            st.info("Signal data will be populated once data sources are connected")
    
    with tab4:
        st.header("About This Dashboard")
        st.markdown("""
        ### India Market Dashboard
        
        A free, educational tool to track Indian economic health and market valuations.
        
        **Data Sources:**
        - Nifty 50 & Sensex: Yahoo Finance (yfinance)
        - Economic Data: RBI, World Bank
        - Market Data: NSE
        
        **Disclaimer:**
        ⚠️ This is for educational purposes only. Not financial advice.
        Always consult a financial advisor before investing.
        
        **Built with:**
        - Streamlit
        - Python
        - Open Source Data
        
        **GitHub:** [india-market-dashboard](https://github.com/sujeetpurbey/india-market-dashboard)
        """)

if __name__ == "__main__":
    main()
