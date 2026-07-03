"""
Main Streamlit app for India Market Dashboard
"""

import streamlit as st
import sys
import os
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import APP_TITLE, APP_ICON, LAYOUT
from src.data_fetcher import DataFetcher
from src.visualizations import create_price_chart
from src.indicators import Indicators

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
        
        try:
            with st.spinner("📥 Fetching latest market data..."):
                fetcher = DataFetcher()
                
                # Fetch data
                nifty_data = fetcher.fetch_nifty_data()
                sensex_data = fetcher.fetch_sensex_data()
                rupee_data = fetcher.fetch_rupee_data()
                
                if nifty_data is not None and len(nifty_data) > 0:
                    # Market Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    # Nifty 50
                    nifty_current = nifty_data['Close'].iloc[-1]
                    nifty_prev = nifty_data['Close'].iloc[-2]
                    nifty_change = ((nifty_current - nifty_prev) / nifty_prev) * 100
                    
                    with col1:
                        st.metric("Nifty 50", f"₹{nifty_current:,.0f}", f"{nifty_change:+.2f}%")
                    
                    # Sensex
                    if sensex_data is not None and len(sensex_data) > 0:
                        sensex_current = sensex_data['Close'].iloc[-1]
                        sensex_prev = sensex_data['Close'].iloc[-2]
                        sensex_change = ((sensex_current - sensex_prev) / sensex_prev) * 100
                        
                        with col2:
                            st.metric("Sensex", f"₹{sensex_current:,.0f}", f"{sensex_change:+.2f}%")
                    
                    # USD/INR
                    if rupee_data is not None and len(rupee_data) > 0:
                        rupee_current = rupee_data['Close'].iloc[-1]
                        rupee_prev = rupee_data['Close'].iloc[-2]
                        rupee_change = ((rupee_current - rupee_prev) / rupee_prev) * 100
                        
                        with col3:
                            st.metric("USD/INR", f"₹{rupee_current:.2f}", f"{rupee_change:+.2f}%")
                    
                    with col4:
                        st.metric("VIX (India)", "Coming Soon", "N/A")
                    
                    st.markdown("---")
                    
                    # Charts
                    st.subheader("📈 Nifty 50 - Last 1 Year")
                    fig = create_price_chart(nifty_data, "Nifty 50 Price Chart")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.subheader("📊 Sensex - Last 1 Year")
                    if sensex_data is not None and len(sensex_data) > 0:
                        fig_sensex = create_price_chart(sensex_data, "Sensex Price Chart")
                        st.plotly_chart(fig_sensex, use_container_width=True)
                else:
                    st.error("❌ Could not fetch Nifty 50 data. Check your internet connection.")
            
        except Exception as e:
            st.error(f"❌ Error fetching data: {str(e)}")
            st.info("Make sure you have an internet connection and yfinance is installed.")
    
    with tab2:
        st.header("Economic & Market Indicators")
        
        try:
            with st.spinner("📊 Calculating indicators..."):
                fetcher = DataFetcher()
                nifty_data = fetcher.fetch_nifty_data()
                
                if nifty_data is not None and len(nifty_data) > 0:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📊 Technical Indicators")
                        
                        # Calculate indicators
                        sma50 = Indicators.calculate_sma(nifty_data['Close'], 50).iloc[-1]
                        sma200 = Indicators.calculate_sma(nifty_data['Close'], 200).iloc[-1]
                        rsi = Indicators.calculate_rsi(nifty_data['Close']).iloc[-1]
                        
                        current_price = nifty_data['Close'].iloc[-1]
                        
                        st.metric("Current Price", f"₹{current_price:,.0f}")
                        st.metric("SMA 50", f"₹{sma50:,.0f}")
                        st.metric("SMA 200", f"₹{sma200:,.0f}")
                        st.metric("RSI (14)", f"{rsi:.1f}")
                        
                        # Signal
                        if sma50 > sma200:
                            st.success("✅ Golden Cross - Bullish")
                        else:
                            st.error("❌ Death Cross - Bearish")
                    
                    with col2:
                        st.subheader("📈 Market Valuation")
                        st.write("**Market Metrics (Coming Soon):**")
                        st.write("- Nifty P/E Ratio")
                        st.write("- Market Cap to GDP")
                        st.write("- Dividend Yield")
                        st.write("- Book Value")
                        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    with tab3:
        st.header("Entry/Exit Signals")
        
        try:
            with st.spinner("🔄 Analyzing market signals..."):
                fetcher = DataFetcher()
                nifty_data = fetcher.fetch_nifty_data()
                
                if nifty_data is not None and len(nifty_data) > 0:
                    st.subheader("Overall Market Signal")
                    
                    # Calculate technical indicators
                    sma50 = Indicators.calculate_sma(nifty_data['Close'], 50).iloc[-1]
                    sma200 = Indicators.calculate_sma(nifty_data['Close'], 200).iloc[-1]
                    rsi = Indicators.calculate_rsi(nifty_data['Close']).iloc[-1]
                    current_price = nifty_data['Close'].iloc[-1]
                    
                    # Generate signals
                    signals = []
                    score = 0
                    
                    if sma50 > sma200:
                        signals.append("✅ SMA 50 > SMA 200 (Bullish)")
                        score += 1
                    else:
                        signals.append("❌ SMA 50 < SMA 200 (Bearish)")
                        score -= 1
                    
                    if rsi < 30:
                        signals.append("✅ RSI < 30 (Oversold - Buy Signal)")
                        score += 1
                    elif rsi > 70:
                        signals.append("❌ RSI > 70 (Overbought - Sell Signal)")
                        score -= 1
                    else:
                        signals.append("🟡 RSI Neutral")
                    
                    # Display signals
                    for signal in signals:
                        st.write(signal)
                    
                    st.markdown("---")
                    
                    # Final recommendation
                    if score > 0:
                        st.success(f"🟢 **BULLISH** - Market looks positive (Score: +{score})")
                    elif score < 0:
                        st.error(f"🔴 **BEARISH** - Market looks negative (Score: {score})")
                    else:
                        st.warning(f"🟡 **NEUTRAL** - Mixed signals (Score: {score})")
                    
                    st.info("⚠️ Disclaimer: This is for educational purposes only. Not financial advice.")
                        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    with tab4:
        st.header("About This Dashboard")
        st.markdown("""
        ### India Market Dashboard 🇮🇳📊
        
        A free, educational tool to track Indian economic health and market valuations.
        
        **Features:**
        - 📈 Real-time Nifty 50 & Sensex data
        - 📊 Technical indicators (SMA, RSI, MACD)
        - 🎯 Entry/Exit trading signals
        - 💹 Market metrics and analysis
        
        **Data Sources:**
        - **Stock Data**: Yahoo Finance (yfinance)
        - **Nifty 50 & Sensex**: NSE via yfinance
        - **Economic Data**: RBI, World Bank, Government of India
        
        **Built With:**
        - Python 🐍
        - Streamlit
        - Pandas & NumPy
        - Plotly Charts
        
        **Disclaimer:**
        ⚠️ This is for **educational purposes only**. 
        This is **NOT financial advice**. 
        Always consult a licensed financial advisor before investing.
        
        **GitHub:** [india-market-dashboard](https://github.com/sujeetpurbey/india-market-dashboard)
        """)

if __name__ == "__main__":
    main()
