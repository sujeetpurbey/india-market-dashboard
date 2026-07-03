"""
Utility functions for the dashboard
"""

import os
import json
from datetime import datetime
from config.settings import CACHE_DIR, CACHE_EXPIRY_HOURS


def ensure_cache_dir():
    """Ensure cache directory exists"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)


def save_to_cache(key, data):
    """Save data to cache"""
    ensure_cache_dir()
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    
    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f)


def load_from_cache(key):
    """Load data from cache"""
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    
    if not os.path.exists(cache_file):
        return None
    
    try:
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        
        # Check if cache is expired
        timestamp = datetime.fromisoformat(cache_data['timestamp'])
        age_hours = (datetime.now() - timestamp).total_seconds() / 3600
        
        if age_hours < CACHE_EXPIRY_HOURS:
            return cache_data['data']
    except Exception as e:
        print(f"Error loading cache: {e}")
    
    return None


def format_currency(value):
    """Format value as currency"""
    return f"₹{value:,.2f}"


def format_percentage(value):
    """Format value as percentage"""
    return f"{value:+.2f}%"


def get_signal_color(signal):
    """Get color for signal"""
    if signal == "BUY":
        return "green"
    elif signal == "SELL":
        return "red"
    else:
        return "orange"
