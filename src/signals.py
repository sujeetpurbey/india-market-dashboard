"""
Signal Analyzer - Generate entry/exit signals based on technical and fundamental analysis
"""

from config.settings import (
    PE_RATIO_UNDERVALUED, PE_RATIO_OVERVALUED,
    MARKET_CAP_TO_GDP_LOW, MARKET_CAP_TO_GDP_HIGH,
    RSI_OVERBOUGHT, RSI_OVERSOLD,
    GDP_GROWTH_GOOD, INFLATION_GOOD, INFLATION_HIGH,
    SMA_FAST, SMA_SLOW
)
from indicators import Indicators


class SignalAnalyzer:
    """Analyze market signals for entry/exit decisions"""
    
    def __init__(self):
        self.bullish_score = 0
        self.bearish_score = 0
        self.signal_reasons = []
    
    def reset_scores(self):
        """Reset scores for new analysis"""
        self.bullish_score = 0
        self.bearish_score = 0
        self.signal_reasons = []
    
    def analyze_valuation(self, pe_ratio):
        """Analyze valuation signal from P/E ratio"""
        if pe_ratio < PE_RATIO_UNDERVALUED:
            self.bullish_score += 2
            self.signal_reasons.append(f"✅ Undervalued: P/E ({pe_ratio:.1f}) < {PE_RATIO_UNDERVALUED}")
        elif pe_ratio > PE_RATIO_OVERVALUED:
            self.bearish_score += 2
            self.signal_reasons.append(f"❌ Overvalued: P/E ({pe_ratio:.1f}) > {PE_RATIO_OVERVALUED}")
        else:
            self.signal_reasons.append(f"⚖️ Fair Valuation: P/E at {pe_ratio:.1f}")
    
    def analyze_market_cap_to_gdp(self, ratio):
        """Analyze Market Cap to GDP ratio signal"""
        if ratio < MARKET_CAP_TO_GDP_LOW:
            self.bullish_score += 1
            self.signal_reasons.append(f"✅ Low Market Cap/GDP: {ratio:.2f}")
        elif ratio > MARKET_CAP_TO_GDP_HIGH:
            self.bearish_score += 1
            self.signal_reasons.append(f"❌ High Market Cap/GDP: {ratio:.2f}")
    
    def analyze_technical(self, close_prices):
        """Analyze technical indicators"""
        # Calculate indicators
        sma_fast = Indicators.calculate_sma(close_prices, SMA_FAST).iloc[-1]
        sma_slow = Indicators.calculate_sma(close_prices, SMA_SLOW).iloc[-1]
        rsi = Indicators.calculate_rsi(close_prices).iloc[-1]
        
        # SMA crossover signal
        if sma_fast > sma_slow:
            self.bullish_score += 1
            self.signal_reasons.append(f"✅ SMA {SMA_FAST} > SMA {SMA_SLOW} (Bullish)")
        else:
            self.bearish_score += 1
            self.signal_reasons.append(f"❌ SMA {SMA_FAST} < SMA {SMA_SLOW} (Bearish)")
        
        # RSI signal
        if rsi < RSI_OVERSOLD:
            self.bullish_score += 1
            self.signal_reasons.append(f"✅ RSI Oversold: {rsi:.1f}")
        elif rsi > RSI_OVERBOUGHT:
            self.bearish_score += 1
            self.signal_reasons.append(f"❌ RSI Overbought: {rsi:.1f}")
    
    def analyze_macro(self, gdp_growth, inflation):
        """Analyze macro indicators"""
        if gdp_growth > GDP_GROWTH_GOOD:
            self.bullish_score += 1
            self.signal_reasons.append(f"✅ Good GDP Growth: {gdp_growth:.1f}%")
        else:
            self.bearish_score += 1
            self.signal_reasons.append(f"❌ Weak GDP Growth: {gdp_growth:.1f}%")
        
        if inflation < INFLATION_GOOD:
            self.bullish_score += 1
            self.signal_reasons.append(f"✅ Controlled Inflation: {inflation:.1f}%")
        elif inflation > INFLATION_HIGH:
            self.bearish_score += 1
            self.signal_reasons.append(f"❌ High Inflation: {inflation:.1f}%")
    
    def get_signal(self):
        """Generate final signal"""
        if self.bullish_score > self.bearish_score:
            return "BUY", "🟢 Bullish"
        elif self.bearish_score > self.bullish_score:
            return "SELL", "🔴 Bearish"
        else:
            return "HOLD", "🟡 Neutral"
    
    def get_signal_strength(self):
        """Get signal strength as percentage"""
        total = self.bullish_score + self.bearish_score
        if total == 0:
            return 0
        return (self.bullish_score / total) * 100
