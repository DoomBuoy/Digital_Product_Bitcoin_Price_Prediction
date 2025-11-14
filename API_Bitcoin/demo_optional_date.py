#!/usr/bin/env python3
"""
Demo script showing the updated Bitcoin Price Prediction API functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from main import predict_bitcoin_price
from datetime import datetime
import asyncio

async def demo_optional_date_functionality():
    """Demonstrate the API with and without date parameter"""
    
    print("🚀 Bitcoin Price Prediction API - Optional Date Demo")
    print("=" * 60)
    
    # Test 1: Without date parameter (should use today's date)
    print("\n📊 Test 1: Prediction WITHOUT date parameter")
    print("-" * 40)
    
    try:
        result1 = await predict_bitcoin_price(
            date=None,  # This should trigger today's date
            open_price=None,
            high_price=None,
            low_price=None,
            close_price=None,
            volume=None,
            market_cap=None
        )
        
        print(f"✅ Success!")
        print(f"📅 Input date used: {result1['input_date']}")
        print(f"🔮 Prediction date: {result1['prediction']['prediction_day_date']}")
        print(f"💰 Predicted high: ${result1['prediction']['Predicted_high']}")
        
        # Verify today's date was used
        today = datetime.now().strftime("%Y-%m-%d")
        if result1['input_date'] == today:
            print(f"✅ Correctly used today's date: {today}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: With date parameter
    print("\n📊 Test 2: Prediction WITH date parameter")
    print("-" * 40)
    
    test_date = "2024-10-25"
    
    try:
        result2 = await predict_bitcoin_price(
            date=test_date,
            open_price=None,
            high_price=None,
            low_price=None,
            close_price=None,
            volume=None,
            market_cap=None
        )
        
        print(f"✅ Success!")
        print(f"📅 Input date used: {result2['input_date']}")
        print(f"🔮 Prediction date: {result2['prediction']['prediction_day_date']}")
        print(f"💰 Predicted high: ${result2['prediction']['Predicted_high']}")
        
        # Verify provided date was used
        if result2['input_date'] == test_date:
            print(f"✅ Correctly used provided date: {test_date}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Demo completed successfully!")
    print("\n📝 Summary:")
    print("• When date=None → Uses today's date automatically")
    print("• When date provided → Uses the provided date")
    print("• Both scenarios fetch real-time data from Kraken + CoinGecko APIs")

if __name__ == "__main__":
    asyncio.run(demo_optional_date_functionality())