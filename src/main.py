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

# Custom CSS for better layout
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    [data-testid="stMetricDelta"] {
        font-size: 14px;
    }
    .stMetric {
        background-color: transparent;
        padding: 10px;
        border-radius: 8px;
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
        st.header("⚙️ Settings")
        
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
        st.header("📈 Market Overview")
        
        try:
            with st.spinner("📥 Fetching latest market data..."):
                fetcher = DataFetcher()
                
                # Fetch data
                nifty_data = fetcher.fetch_nifty_data()
                sensex_data = fetcher.fetch_sensex_data()
                rupee_data = fetcher.fetch_rupee_data()
                
                if nifty_data is not None and len(nifty_data) > 0:
                    # Market Metrics in proper columns - using flexible layout
                    st.subheader("📊 Key Market Indices")
                    
                    # Create metrics separately to ensure inline display
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns([1, 1, 1, 1], gap="small")
                    
                    # Nifty 50
                    nifty_current = float(nifty_data['Close'].iloc[-1])
                    nifty_prev = float(nifty_data['Close'].iloc[-2])
                    nifty_change = ((nifty_current - nifty_prev) / nifty_prev) * 100
                    
                    with metric_col1:
                        st.metric(
                            label="Nifty 50",
                            value=f"₹{nifty_current:,.0f}",
                            delta=f"{nifty_change:+.2f}%"
                        )
                    
                    # Sensex
                    if sensex_data is not None and len(sensex_data) > 0:
                        sensex_current = float(sensex_data['Close'].iloc[-1])
                        sensex_prev = float(sensex_data['Close'].iloc[-2])
                        sensex_change = ((sensex_current - sensex_prev) / sensex_prev) * 100
                        
                        with metric_col2:
                            st.metric(
                                label="Sensex",
                                value=f"₹{sensex_current:,.0f}",
                                delta=f"{sensex_change:+.2f}%"
                            )
                    
                    # USD/INR
                    if rupee_data is not None and len(rupee_data) > 0:
                        rupee_current = float(rupee_data['Close'].iloc[-1])
                        rupee_prev = float(rupee_data['Close'].iloc[-2])
                        rupee_change = ((rupee_current - rupee_prev) / rupee_prev) * 100
                        
                        with metric_col3:
                            st.metric(
                                label="USD/INR",
                                value=f"₹{rupee_current:.2f}",
                                delta=f"{rupee_change:+.2f}%"
                            )
                    
                    # VIX
                    with metric_col4:
                        st.metric(
                            label="VIX (India)",
                            value="Coming Soon",
                            delta="—"
                        )
                    
                    st.markdown("---")
                    
                    # Charts
                    st.subheader("📈 Price Charts")
                    
                    chart_col1, chart_col2 = st.columns(2)
                    
                    with chart_col1:
                        st.write("**Nifty 50 - Last 1 Year**")
                        fig = create_price_chart(nifty_data, "Nifty 50")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with chart_col2:
                        st.write("**Sensex - Last 1 Year**")
                        if sensex_data is not None and len(sensex_data) > 0:
                            fig_sensex = create_price_chart(sensex_data, "Sensex")
                            st.plotly_chart(fig_sensex, use_container_width=True)
                    
                    # USD/INR Chart - Full width
                    st.write("**USD/INR Exchange Rate - Last 1 Year**")
                    if rupee_data is not None and len(rupee_data) > 0:
                        fig_rupee = create_price_chart(rupee_data, "USD/INR")
                        st.plotly_chart(fig_rupee, use_container_width=True)
                    
                else:
                    st.error("❌ Could not fetch market data. Check your internet connection.")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("If this persists, try refreshing the page or check your internet connection.")
    
    with tab2:
        st.header("📊 Technical Indicators")
        
        try:
            with st.spinner("📊 Calculating indicators..."):
                fetcher = DataFetcher()
                nifty_data = fetcher.fetch_nifty_data()
                
                if nifty_data is not None and len(nifty_data) > 0:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📈 Nifty 50 Technicals")
                        
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
                            st.success("✅ **Golden Cross** - Bullish Trend")
                        else:
                            st.error("❌ **Death Cross** - Bearish Trend")
                    
                    with col2:
                        st.subheader("📋 Market Signals")
                        
                        st.write("**RSI Interpretation:**")
                        if rsi > 70:
                            st.warning(f"⚠️ RSI > 70: OVERBOUGHT (Sell Signal)")
                        elif rsi < 30:
                            st.info(f"ℹ️ RSI < 30: OVERSOLD (Buy Signal)")
                        else:
                            st.info(f"ℹ️ RSI {rsi:.1f}: NEUTRAL")
                        
                        st.write("\n**Price vs Moving Averages:**")
                        if current_price > sma50:
                            st.success(f"✅ Price above SMA50")
                        else:
                            st.error(f"❌ Price below SMA50")
                        
                        if current_price > sma200:
                            st.success(f"✅ Price above SMA200 (Long-term Bullish)")
                        else:
                            st.error(f"❌ Price below SMA200 (Long-term Bearish)")
                        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    with tab3:
        st.header("🎯 Trading Signals")
        
        try:
            with st.spinner("🔄 Analyzing market signals..."):
                fetcher = DataFetcher()
                nifty_data = fetcher.fetch_nifty_data()
                
                if nifty_data is not None and len(nifty_data) > 0:
                    st.subheader("📊 Overall Market Signal")
                    
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
                        signals.append("🟡 RSI Neutral (30-70 range)")
                        score += 0
                    
                    if current_price > sma50:
                        signals.append("✅ Price > SMA50 (Short-term Bullish)")
                        score += 0.5
                    else:
                        signals.append("❌ Price < SMA50 (Short-term Bearish)")
                        score -= 0.5
                    
                    # Display signals
                    st.write("**Signal Details:**")
                    for signal in signals:
                        st.write(signal)
                    
                    st.markdown("---")
                    
                    # Final recommendation
                    if score > 1:
                        st.success(f"🟢 **STRONG BUY** - Market looks very positive (Score: +{score:.1f})")
                    elif score > 0:
                        st.success(f"🟢 **BULLISH** - Market looks positive (Score: +{score:.1f})")
                    elif score < -1:
                        st.error(f"🔴 **STRONG SELL** - Market looks very negative (Score: {score:.1f})")
                    elif score < 0:
                        st.error(f"🔴 **BEARISH** - Market looks negative (Score: {score:.1f})")
                    else:
                        st.warning(f"🟡 **NEUTRAL** - Mixed signals (Score: {score:.1f})")
                    
                    st.info("⚠️ **Disclaimer**: This is for educational purposes only. Not financial advice. Always consult a financial advisor.")
                        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    with tab4:
        st.header("📖 About This Dashboard")
        st.markdown("""
        ### 🇮🇳 India Market Dashboard
        
        A free, open-source educational tool to track Indian economic health and market valuations.
        
        ---
        
        ### ✨ Features
        
        - 📈 **Real-time Market Data**: Live Nifty 50, Sensex, and USD/INR prices
        - 📊 **Technical Analysis**: SMA 50/200, RSI indicators
        - 🎯 **Trading Signals**: Buy/Sell recommendations based on technical analysis
        - 📉 **Interactive Charts**: Plotly-powered price charts with trends
        - 💾 **Smart Caching**: Data cached for 24 hours to avoid API rate limits
        - 🔄 **Fallback Demo Data**: Works even when live data is unavailable
        
        ---
        
        ### 📡 Data Sources
        
        - **Stock Market Data**: Yahoo Finance via yfinance library
        - **Nifty 50 Ticker**: ^NSEI
        - **Sensex Ticker**: ^BSESN
        - **USD/INR Ticker**: USDINR=X
        
        ---
        
        ### 🛠️ Built With
        
        - **Python** 🐍
        - **Streamlit** - Web app framework
        - **Pandas & NumPy** - Data manipulation
        - **Plotly** - Interactive charts
        - **yfinance** - Stock data fetching
        
        ---
        
        ### ⚠️ Important Disclaimer
        
        - ❌ **NOT financial advice**
        - 📚 **Educational purposes only**
        - 🎓 **For learning and research**
        - 💼 **Always consult a licensed financial advisor before investing**
        
        ---
        
        ### 📂 Technical Details
        
        - Data Period: 5 years of historical data
        - Data Interval: Daily (1D)
        - Cache Duration: 24 hours
        - Request Delay: 2 seconds between API calls (to avoid rate limiting)
        
        ---
        
        ### 🔗 Links
        
        - **GitHub**: [india-market-dashboard](https://github.com/sujeetpurbey/india-market-dashboard)
        - **Creator**: Sujeet Purbey
        
        """)

if __name__ == "__main__":
    main()
