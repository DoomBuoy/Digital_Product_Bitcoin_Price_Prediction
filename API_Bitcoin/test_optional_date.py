#!/usr/bin/env python3
"""
Test script to verify the updated prediction endpoint with optional date parameter
"""

import requests
import json
from datetime import datetime

def test_prediction_without_date():
    """Test the prediction endpoint without providing a date"""
    try:
        # Test the endpoint without date parameter
        url = "http://localhost:8000/predict/Bitcoin"
        
        print("🔄 Testing prediction endpoint without date parameter...")
        print(f"🌐 URL: {url}")
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! API responded correctly")
            print(f"📅 Input date used: {data.get('input_date')}")
            print(f"🔮 Prediction: {json.dumps(data.get('prediction'), indent=2)}")
            
            # Verify that today's date was used
            today = datetime.now().strftime("%Y-%m-%d")
            if data.get('input_date') == today:
                print(f"✅ Correctly used today's date: {today}")
            else:
                print(f"⚠️ Expected today's date ({today}) but got: {data.get('input_date')}")
                
        else:
            print(f"❌ API returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_prediction_with_date():
    """Test the prediction endpoint with a date parameter"""
    try:
        test_date = "2024-10-25"
        url = f"http://localhost:8000/predict/Bitcoin?date={test_date}"
        
        print(f"\n🔄 Testing prediction endpoint with date parameter: {test_date}")
        print(f"🌐 URL: {url}")
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! API responded correctly")
            print(f"📅 Input date used: {data.get('input_date')}")
            print(f"🔮 Prediction: {json.dumps(data.get('prediction'), indent=2)}")
            
            if data.get('input_date') == test_date:
                print(f"✅ Correctly used provided date: {test_date}")
            else:
                print(f"⚠️ Expected provided date ({test_date}) but got: {data.get('input_date')}")
                
        else:
            print(f"❌ API returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Bitcoin Price Prediction API with Optional Date Parameter")
    print("=" * 70)
    
    # Test without date (should use today's date)
    test_prediction_without_date()
    
    # Test with date (should use provided date)
    test_prediction_with_date()
    
    print("\n" + "=" * 70)
    print("✅ Test completed!")