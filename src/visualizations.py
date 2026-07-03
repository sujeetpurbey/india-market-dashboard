"""
Visualizations - Create charts and visual components for the dashboard
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config.settings import COLOR_BULLISH, COLOR_BEARISH, COLOR_NEUTRAL


def create_market_metrics(nifty_data, sensex_data):
    """Create market metrics cards"""
    metrics = {}
    
    if nifty_data is not None and len(nifty_data) > 0:
        metrics['nifty_current'] = nifty_data['Close'].iloc[-1]
        metrics['nifty_change'] = ((nifty_data['Close'].iloc[-1] - nifty_data['Close'].iloc[-2]) / 
                                    nifty_data['Close'].iloc[-2] * 100)
    
    if sensex_data is not None and len(sensex_data) > 0:
        metrics['sensex_current'] = sensex_data['Close'].iloc[-1]
        metrics['sensex_change'] = ((sensex_data['Close'].iloc[-1] - sensex_data['Close'].iloc[-2]) / 
                                     sensex_data['Close'].iloc[-2] * 100)
    
    return metrics


def create_signal_gauge(signal_strength):
    """Create a gauge chart for signal strength"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=signal_strength,
        title={'text': "Market Signal Strength"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': COLOR_BEARISH},
                {'range': [30, 70], 'color': COLOR_NEUTRAL},
                {'range': [70, 100], 'color': COLOR_BULLISH}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    return fig


def create_price_chart(data, title="Price Chart"):
    """Create a price chart with moving averages"""
    fig = go.Figure()
    
    # Add candlestick chart
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='blue', width=2)
    ))
    
    # Add SMA
    sma50 = data['Close'].rolling(window=50).mean()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=sma50,
        mode='lines',
        name='SMA 50',
        line=dict(color='orange', width=1, dash='dash')
    ))
    
    sma200 = data['Close'].rolling(window=200).mean()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=sma200,
        mode='lines',
        name='SMA 200',
        line=dict(color='red', width=1, dash='dash')
    ))
    
    fig.update_layout(
        title=title,
        yaxis_title='Price (₹)',
        xaxis_title='Date',
        hovermode='x unified',
        height=500
    )
    
    return fig


def create_indicator_table(indicators_dict):
    """Create a table of indicators"""
    df = pd.DataFrame([
        {'Indicator': k, 'Value': v} 
        for k, v in indicators_dict.items()
    ])
    return df
