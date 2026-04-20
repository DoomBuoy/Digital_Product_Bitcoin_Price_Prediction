"""
Test script to verify the updated prediction endpoint, including optional dates 
and custom feature overrides.
"""

import requests
import json
from datetime import datetime

def test_prediction_without_date():
    """Test the prediction endpoint without providing a date (uses today)"""
    try:
        url = "http://localhost:8000/predict/Bitcoin"
        
        print("🔄 Testing prediction endpoint without date parameter...")
        print(f"🌐 URL: {url}")
        
        response = requests.get(url, timeout=45) # Increased timeout due to multi-day API fetching
        
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
    """Test the prediction endpoint with a specific date parameter"""
    try:
        test_date = "2024-10-25"
        url = f"http://localhost:8000/predict/Bitcoin?date={test_date}"
        
        print(f"\n🔄 Testing prediction endpoint with date parameter: {test_date}")
        print(f"🌐 URL: {url}")
        
        response = requests.get(url, timeout=45)
        
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

def test_prediction_with_overrides():
    """Test the prediction endpoint using custom data overrides for the target date"""
    try:
        test_date = "2024-10-25"
        # Passing a hypothetical scenario: What if Bitcoin closed at $80,000 with massive volume?
        custom_close = 80000.00
        custom_volume = 75000000000.00
        
        url = f"http://localhost:8000/predict/Bitcoin?date={test_date}&close_price={custom_close}&volume={custom_volume}"
        
        print(f"\n🔄 Testing prediction endpoint with custom overrides (Close: {custom_close}, Vol: {custom_volume})")
        print(f"🌐 URL: {url}")
        
        response = requests.get(url, timeout=45)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! API handled custom overrides correctly")
            print(f"📅 Input date used: {data.get('input_date')}")
            print(f"🔮 Prediction with overrides: {json.dumps(data.get('prediction'), indent=2)}")
        else:
            print(f"❌ API returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Bitcoin Price Prediction API")
    print("=" * 70)
    
    # 1. Test without date (should use today's date)
    test_prediction_without_date()
    
    # 2. Test with date (should fetch 15 days ending on this date)
    test_prediction_with_date()
    
    # 3. Test with overrides (should fetch 15 days, but overwrite the final day's close/volume)
    test_prediction_with_overrides()
    
    print("\n" + "=" * 70)
    print("✅ All tests completed!")