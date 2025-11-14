import requests
import pandas as pd
import streamlit as st
from datetime import datetime
import yfinance as yf

# Define our main cryptocurrency
MAIN_CRYPTOS = {
    "bitcoin": {
        "symbol": "BTC",
        "name": "Bitcoin",
        "icon": "₿",
        "color": "#F7931A",
        "yf_symbol": "BTC-USD"
    }
}

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_crypto_data():
    """Get data for our four main cryptocurrencies"""
    crypto_data = []
    
    # Try to get real data from CoinGecko
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_market_cap': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            for crypto_id, crypto_info in MAIN_CRYPTOS.items():
                if crypto_id in data:
                    crypto_data.append({
                        'id': crypto_id,
                        'symbol': crypto_info['symbol'],
                        'name': crypto_info['name'],
                        'icon': crypto_info['icon'],
                        'color': crypto_info['color'],
                        'current_price': data[crypto_id].get('usd', 0),
                        'price_change_percentage_24h': data[crypto_id].get('usd_24h_change', 0),
                        'market_cap': data[crypto_id].get('usd_market_cap', 0)
                    })
        else:
            raise Exception("API request failed")
            
    except Exception as e:
        # Fallback data if API fails
        st.warning("Using sample data - API unavailable")
        crypto_data = [
            {'id': 'bitcoin', 'symbol': 'BTC', 'name': 'Bitcoin', 'icon': '₿', 'color': '#F7931A', 'current_price': 43250, 'price_change_percentage_24h': 2.5, 'market_cap': 850000000000}
        ]
    
    return crypto_data

@st.cache_data(ttl=600)
def get_price_history(yf_symbol, period="7d"):
    """Get price history using yfinance"""
    try:
        # Convert period to yfinance format
        period_map = {"7d": "7d", "30d": "1mo", "90d": "3mo", "1y": "1y"}
        yf_period = period_map.get(period, "7d")
        
        # Get data from yfinance
        crypto = yf.Ticker(yf_symbol)
        hist = crypto.history(period=yf_period)
        
        if not hist.empty:
            return hist
        else:
            # Generate sample data if no real data available
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            sample_data = pd.DataFrame({
                'Close': [100 + i*2 + (i%3)*10 for i in range(30)]
            }, index=dates)
            return sample_data
            
    except:
        # Generate sample data as fallback
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        sample_data = pd.DataFrame({
            'Close': [100 + i*2 + (i%3)*10 for i in range(30)]
        }, index=dates)
        return sample_data