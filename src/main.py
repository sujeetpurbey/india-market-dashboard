import streamlit as st
from config.settings import APP_TITLE, APP_ICON, LAYOUT
from src.data_fetcher import DataFetcher
from src.visualizations import create_price_chart
from src.indicators import Indicators

# Cache data to avoid repeated API calls
@st.cache_data(ttl=3600)
def get_market_data():
    fetcher = DataFetcher()
    return {
        "nifty": fetcher.fetch_nifty_data(),
        "sensex": fetcher.fetch_sensex_data(),
        "rupee": fetcher.fetch_rupee_data()
    }

def safe_metric(label, data, col, currency=False):
    try:
        if data is not None and len(data) > 1:
            current = float(data['Close'].iloc[-1])
            prev = float(data['Close'].iloc[-2])
            change = ((current - prev) / prev) * 100
            value = f"₹{current:,.2f}" if currency else f"{current:,.2f}"
            col.metric(label=label, value=value, delta=f"{change:+.2f}%")
        else:
            col.metric(label=label, value="Data Unavailable", delta="—")
    except Exception as e:
        col.metric(label=label, value="Error", delta="—")
        st.error(f"{label} metric failed: {e}")

def safe_chart(data, title):
    if data is not None and len(data) > 0:
        fig = create_price_chart(data, title)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No data available for {title}")

def safe_indicators(data):
    if data is not None and len(data) >= 200:
        sma50 = Indicators.calculate_sma(data['Close'], 50).iloc[-1]
        sma200 = Indicators.calculate_sma(data['Close'], 200).iloc[-1]
        rsi = Indicators.calculate_rsi(data['Close']).iloc[-1]
        return sma50, sma200, rsi
    else:
        st.warning("Not enough data for SMA200/RSI")
        return None, None, None

def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=LAYOUT,
        initial_sidebar_state="expanded"
    )

    st.title(f"{APP_ICON} {APP_TITLE}")
    st.markdown("Track Indian economic indicators, market health, and get entry/exit signals")
    st.markdown("---")

    with st.sidebar:
        st.header("⚙️ Settings")
        refresh_interval = st.selectbox("Refresh Data Every:", ["1 hour", "4 hours", "Daily"])
        show_technical = st.checkbox("Show Technical Indicators", value=True)
        show_macro = st.checkbox("Show Macro Indicators", value=True)
        show_signals = st.checkbox("Show Entry/Exit Signals", value=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Market Overview", "📊 Indicators", "🎯 Signals", "📖 About"])

    # Market Overview
    with tab1:
        st.header("📈 Market Overview")
        market_data = get_market_data()
        nifty_data, sensex_data, rupee_data = market_data["nifty"], market_data["sensex"], market_data["rupee"]

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns([1, 1, 1, 1], gap="small")
        safe_metric("Nifty 50", nifty_data, metric_col1, currency=True)
        safe_metric("Sensex", sensex_data, metric_col2, currency=True)
        safe_metric("USD/INR", rupee_data, metric_col3, currency=True)
        metric_col4.metric(label="VIX (India)", value="Coming Soon", delta="—")

        st.markdown("---")
        st.subheader("📈 Price Charts")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1: safe_chart(nifty_data, "Nifty 50")
        with chart_col2: safe_chart(sensex_data, "Sensex")
        st.write("**USD/INR Exchange Rate - Last 1 Year**")
        safe_chart(rupee_data, "USD/INR")

    # Indicators
    with tab2:
        st.header("📊 Technical Indicators")
        nifty_data = market_data["nifty"]
        sma50, sma200, rsi = safe_indicators(nifty_data)
        if sma50 and sma200 and rsi:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📈 Nifty 50 Technicals")
                current_price = nifty_data['Close'].iloc[-1]
                st.metric("Current Price", f"₹{current_price:,.0f}")
                st.metric("SMA 50", f"₹{sma50:,.0f}")
                st.metric("SMA 200", f"₹{sma200:,.0f}")
                st.metric("RSI (14)", f"{rsi:.1f}")
                if sma50 > sma200:
                    st.success("✅ Golden Cross - Bullish Trend")
                else:
                    st.error("❌ Death Cross - Bearish Trend")
            with col2:
                st.subheader("📋 Market Signals")
                if rsi > 70: st.warning("⚠️ RSI > 70: OVERBOUGHT (Sell Signal)")
                elif rsi < 30: st.info("ℹ️ RSI < 30: OVERSOLD (Buy Signal)")
                else: st.info(f"ℹ️ RSI {rsi:.1f}: NEUTRAL")
                if current_price > sma50: st.success("✅ Price above SMA50")
                else: st.error("❌ Price below SMA50")
                if current_price > sma200: st.success("✅ Price above SMA200 (Long-term Bullish)")
                else: st.error("❌ Price below SMA200 (Long-term Bearish)")

    # Signals
    with tab3:
        st.header("🎯 Trading Signals")
        nifty_data = market_data["nifty"]
        sma50, sma200, rsi = safe_indicators(nifty_data)
        if sma50 and sma200 and rsi:
            current_price = nifty_data['Close'].iloc[-1]
            signals, score = [], 0
            signals.append("✅ SMA 50 > SMA 200 (Bullish)" if sma50 > sma200 else "❌ SMA 50 < SMA 200 (Bearish)")
            score += 1 if sma50 > sma200 else -1
            if rsi < 30: signals.append("✅ RSI < 30 (Oversold - Buy Signal)"); score += 1
            elif rsi > 70: signals.append("❌ RSI > 70 (Overbought - Sell Signal)"); score -= 1
            else: signals.append("🟡 RSI Neutral (30-70 range)")
            if current_price > sma50: signals.append("✅ Price > SMA50 (Short-term Bullish)"); score += 0.5
            else: signals.append("❌ Price < SMA50 (Short-term Bearish)"); score -= 0.5
            st.write("**Signal Details:**")
            for s in signals: st.write(s)
            st.markdown("---")
            if score > 1: st.success(f"🟢 STRONG BUY (Score: +{score:.1f})")
            elif score > 0: st.success(f"🟢 BULLISH (Score: +{score:.1f})")
            elif score < -1: st.error(f"🔴 STRONG SELL (Score: {score:.1f})")
            elif score < 0: st.error(f"🔴 BEARISH (Score: {score:.1f})")
            else: st.warning(f"🟡 NEUTRAL (Score: {score:.1f})")
            st.info("⚠️ Disclaimer: Educational purposes only. Not financial advice.")

    # About
    with tab4:
        st.header("📖 About This Dashboard")
        st.markdown("Open-source tool to track Indian market health. Built with Python, Streamlit, Plotly, and yfinance.")

if __name__ == "__main__":
    main()
