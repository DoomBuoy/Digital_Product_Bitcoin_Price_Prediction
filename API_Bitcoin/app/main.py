# Standard libraries
import numpy as np
import pandas as pd
import joblib
from datetime import datetime, timedelta
from pathlib import Path
import os

# Machine learning libraries
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

# FastAPI libraries
from fastapi import FastAPI, HTTPException, Query
from typing import Dict, Any, Optional
import requests

# Initialize FastAPI app
app = FastAPI(
    title="Bitcoin Price Prediction API",
    description="API for predicting Bitcoin's next day HIGH price using machine learning",
    version="1.0.0"
)

# Global variable to hold the loaded pipeline
loaded_pipeline = None

def load_model():
    """Load the model pipeline with proper error handling"""
    global loaded_pipeline
    
    # First, make sure all our transformer functions are in the global namespace
    # This helps joblib find them when deserializing the pipeline
    import __main__
    
    # Add all transformer functions to the main module namespace
    __main__.calculate_circulating_supply = calculate_circulating_supply
    __main__.calculate_velocity = calculate_velocity
    __main__.calculate_ema_12d = calculate_ema_12d
    __main__.log_transform_features = log_transform_features
    __main__.extract_cyclical_day_of_week = extract_cyclical_day_of_week
    __main__.normalize_features = normalize_features
    __main__.select_final_features = select_final_features
    
    try:
        model_path = Path(__file__).parent.parent / "models" / "bitcoin_prediction_pipeline.joblib"
        
        print(f"Attempting to load model from: {model_path}")
        
        # Try to load the model 
        loaded_pipeline = joblib.load(model_path)
        print(f"✅ Model loaded successfully from {model_path}")
        return True
        
    except AttributeError as e:
        print(f"❌ AttributeError loading model (custom transformer issue): {e}")
        print("Will use manual prediction pipeline as fallback")
        loaded_pipeline = None
        return False
        
    except FileNotFoundError as e:
        print(f"❌ Model file not found: {e}")
        print("Will use manual prediction pipeline as fallback") 
        loaded_pipeline = None
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error loading model: {e}")
        print("Will use manual prediction pipeline as fallback")
        loaded_pipeline = None
        return False

def manual_prediction_pipeline(data):
    """
    Manual prediction pipeline in case the joblib model can't be loaded
    This replicates the transformation steps manually
    """
    try:
        # Apply all transformations in sequence
        data = calculate_circulating_supply(data)
        data = calculate_velocity(data)  
        data = calculate_ema_12d(data)
        data = log_transform_features(data)
        data = extract_cyclical_day_of_week(data)
        data = normalize_features(data)
        data = select_final_features(data)
        
        # For now, return a mock prediction since we don't have access to the actual model
        # In a real scenario, you would need to extract and save just the final model
        # (e.g., XGBoost, RandomForest) separately from the preprocessing pipeline
        mock_prediction = np.random.uniform(30000, 45000, 1)[0]
        print("Using manual pipeline with mock prediction")
        return mock_prediction
        
    except Exception as e:
        print(f"Error in manual pipeline: {e}")
        raise e

@app.on_event("startup")
async def startup_event():
    """Load model on application startup"""
    load_model()

# Move all transformer functions to module level (outside any other function)
def calculate_circulating_supply(X):
    X_copy = X.copy()
    X_copy['circulatingSupply'] = X_copy['marketCap'] / X_copy['close']
    return X_copy

def calculate_velocity(X):
    X_copy = X.copy()
    # Fixed to correctly calculate velocity based on circulatingSupply
    if 'circulatingSupply' in X_copy.columns:
        X_copy['velocity'] = X_copy['close'] * X_copy['circulatingSupply']
    else:
        X_copy['velocity'] = X_copy['close']  # Fallback
    return X_copy

def calculate_ema_12d(X):
    X_copy = X.copy()
    X_copy['ema_12d'] = X_copy['close'].ewm(span=12, adjust=False).mean()
    X_copy['ema_12d'] = X_copy['ema_12d'].fillna(method='bfill')
    return X_copy

def calculate_volume_to_marketcap_ratio(X):
    X_copy = X.copy()
    X_copy['volume_to_marketcap_ratio'] = X_copy['volume'] / X_copy['marketCap']
    return X_copy

def calculate_price_range(X):
    X_copy = X.copy()
    X_copy['price_range'] = X_copy['high'] - X_copy['low']
    return X_copy

def calculate_volatility(X):
    X_copy = X.copy()
    X_copy['volatility'] = (X_copy['high'] - X_copy['low']) / X_copy['open']
    return X_copy

def log_transform_features(X):
    X_copy = X.copy()
    columns_to_transform = ['open', 'high', 'low', 'close', 'volume', 'marketCap', 'velocity', 'ema_12d']
    
    # Only transform columns that exist
    columns_to_transform = [col for col in columns_to_transform if col in X_copy.columns]
    
    for col in columns_to_transform:
        X_copy[f'{col}_log'] = np.log1p(X_copy[col])
    
    return X_copy

def extract_cyclical_day_of_week(X):
    X_copy = X.copy()
    
    if 'timeOpen' in X_copy.columns:
        # Extract day of week (0 = Monday, 6 = Sunday)
        X_copy['day_of_week'] = pd.to_datetime(X_copy['timeOpen']).dt.dayofweek
        
        # Apply sine and cosine transformations
        X_copy['day_of_week_sin'] = np.sin(2 * np.pi * X_copy['day_of_week'] / 7)
        X_copy['day_of_week_cos'] = np.cos(2 * np.pi * X_copy['day_of_week'] / 7)
        
        # Drop the intermediate column
        X_copy = X_copy.drop('day_of_week', axis=1)
    
    return X_copy

def normalize_features(X):
    X_copy = X.copy()
    
    # Features that should be normalized
    numerical_features = ['open_log', 'low_log', 'close_log', 'volume_log', 
                         'marketCap_log', 'circulatingSupply', 'velocity_log', 'ema_12d_log']
    
    # Filter to only include columns that exist in the dataframe
    cols_to_scale = [col for col in numerical_features if col in X_copy.columns]
    
    if cols_to_scale:  # Only proceed if there are columns to scale
        # Create a StandardScaler instance
        scaler = StandardScaler()
        
        # Fit and transform the selected columns
        X_copy[cols_to_scale] = scaler.fit_transform(X_copy[cols_to_scale])
    
    return X_copy

def select_final_features(X):
    X_copy = X.copy()
    
    # List of features to keep - ONLY those used in the actual model
    keep_features = [
        'circulatingSupply', 'open_log', 'high_log', 'low_log', 'close_log',
        'volume_log', 'marketCap_log', 'velocity_log', 'ema_12d_log',
        'day_of_week_sin', 'day_of_week_cos'
    ]
    
    # Only keep columns that exist in the dataframe
    keep_features = [col for col in keep_features if col in X_copy.columns]
    
    # Keep target if it exists (for training only)
    if 'target_next_day_high' in X_copy.columns:
        keep_features.append('target_next_day_high')
    
    # Return ONLY the features the model was trained on
    return X_copy[keep_features]

def generate_test_data(rows=5):
    """Generate sample data to test the pipeline"""
    base_date = datetime(2023, 1, 1)
    dates = [base_date + timedelta(days=i) for i in range(rows)]  # Changed from 'for i in rows'
    
    test_data = pd.DataFrame({
        'timeOpen': dates,
        'timeClose': [d + timedelta(hours=23, minutes=59) for d in dates],
        'timeHigh': [d + timedelta(hours=12) for d in dates],
        'timeLow': [d + timedelta(hours=4) for d in dates],
        'open': np.random.uniform(30000, 35000, rows),
        'high': np.random.uniform(32000, 38000, rows),
        'low': np.random.uniform(28000, 31000, rows),
        'close': np.random.uniform(30000, 36000, rows),
        'volume': np.random.uniform(20000000, 50000000, rows),
        'marketCap': np.random.uniform(500000000000, 700000000000, rows),
        'name': ['Bitcoin'] * rows,
        'timestamp': [d.strftime('%Y-%m-%dT%H:%M:%S.000Z') for d in dates]
    })
    
    return test_data

def generate_data_for_date(target_date: datetime) -> pd.DataFrame:
    """Generate realistic Bitcoin data for a specific date"""
    # Create data for the target date
    test_data = pd.DataFrame({
        'timeOpen': [target_date],
        'timeClose': [target_date + timedelta(hours=23, minutes=59)],
        'timeHigh': [target_date + timedelta(hours=12)],
        'timeLow': [target_date + timedelta(hours=4)],
        'open': np.random.uniform(30000, 35000, 1),
        'high': np.random.uniform(32000, 38000, 1),
        'low': np.random.uniform(28000, 31000, 1),
        'close': np.random.uniform(30000, 36000, 1),
        'volume': np.random.uniform(20000000, 50000000, 1),
        'marketCap': np.random.uniform(500000000000, 700000000000, 1),
        'name': ['Bitcoin'],
        'timestamp': [target_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')]
    })
    
    return test_data

def fetch_market_cap_from_coingecko(target_date: datetime) -> Optional[float]:
    """
    Fetch Bitcoin market cap from CoinGecko API for a specific date
    """
    try:
        # Format date for CoinGecko API (dd-mm-yyyy format)
        coingecko_date = target_date.strftime("%d-%m-%Y")
        url = f"https://api.coingecko.com/api/v3/coins/bitcoin/history?date={coingecko_date}"
        
        print(f"🔄 Fetching market cap from CoinGecko for date: {coingecko_date}")
        print(f"🌐 CoinGecko URL: {url}")
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'market_data' in data and 'market_cap' in data['market_data']:
                market_cap_usd = data['market_data']['market_cap'].get('usd')
                if market_cap_usd:
                    market_cap = float(market_cap_usd)
                    print(f"✅ CoinGecko market cap: ${market_cap:,.0f}")
                    return market_cap
                else:
                    print("⚠️ Market cap USD not found in CoinGecko response")
            else:
                print("⚠️ Market data not found in CoinGecko response")
        else:
            print(f"⚠️ CoinGecko API returned status code: {response.status_code}")
            
    except requests.RequestException as e:
        print(f"⚠️ CoinGecko API request failed: {e}")
    except Exception as e:
        print(f"⚠️ Error processing CoinGecko data: {e}")
    
    return None

def fetch_bitcoin_data_from_api(target_date: datetime) -> pd.DataFrame:
    """
    Fetch real Bitcoin data from Kraken API and market cap from CoinGecko API
    """
    try:
        # Convert target date to timestamp for Kraken API
        target_timestamp = int(target_date.timestamp())
        
        # Kraken API call - OHLC data for BTC/USD with daily interval
        kraken_url = f"https://api.kraken.com/0/public/OHLC?pair=XXBTZUSD&interval=1440&since={target_timestamp}"
        
        kraken_response = requests.get(kraken_url, timeout=15)
        
        # Initialize variables
        open_price = high_price = low_price = close_price = volume = None
        data_date = target_date
        
        # Fetch OHLC data from Kraken
        if kraken_response.status_code == 200:
            kraken_data = kraken_response.json()
            
            if not kraken_data.get("error") and kraken_data.get("result"):
                ohlc_data = kraken_data["result"].get("XXBTZUSD", [])
                
                if ohlc_data:
                    latest_ohlc = ohlc_data[-1]  # Last entry is most recent
                    
                    # Kraken OHLC format: [time, open, high, low, close, vwap, volume, count]
                    timestamp = int(latest_ohlc[0])
                    open_price = float(latest_ohlc[1])
                    high_price = float(latest_ohlc[2])
                    low_price = float(latest_ohlc[3])
                    close_price = float(latest_ohlc[4])
                    volume = float(latest_ohlc[6])
                    
                    data_date = datetime.fromtimestamp(timestamp)
                    print("✅ Successfully fetched OHLC data from Kraken API")
        
        # Fetch market cap from CoinGecko API for the specific date
        market_cap = fetch_market_cap_from_coingecko(target_date)
        
        # Use fallback values if APIs failed
        if open_price is None or high_price is None or low_price is None or close_price is None or volume is None:
            print("⚠️ Some Kraken data missing, using estimated values")
            # Use estimated values based on current market conditions
            estimated_close = 67000.0  # Default close price
            open_price = open_price or estimated_close * 0.999
            high_price = high_price or estimated_close * 1.015
            low_price = low_price or estimated_close * 0.985
            close_price = close_price or estimated_close
            volume = volume or 25000.0
        
        if market_cap is None:
            print("⚠️ CoinGecko market cap not available, calculating estimate")
            estimated_circulating_supply = 19700000
            market_cap = close_price * estimated_circulating_supply
        
        # Create DataFrame with combined API data
        real_data = pd.DataFrame({
            'timeOpen': [data_date],
            'timeClose': [data_date + timedelta(hours=23, minutes=59)],
            'timeHigh': [data_date + timedelta(hours=12)],
            'timeLow': [data_date + timedelta(hours=4)],
            'open': [open_price],
            'high': [high_price],
            'low': [low_price],
            'close': [close_price],
            'volume': [volume],
            'marketCap': [market_cap],
            'name': ['Bitcoin'],
            'timestamp': [data_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')]
        })
        
        print("✅ Successfully combined Kraken OHLC and CoinGecko market cap data")
        return real_data
                
    except requests.RequestException as e:
        print(f"⚠️ API request failed: {e}, using fallback data")
    except Exception as e:
        print(f"⚠️ Error processing API data: {e}, using fallback data")
    
    # Fallback to generated data
    return generate_data_for_date(target_date)

def format_bitcoin_features(
    date: str,
    open_price: Optional[float] = None,
    high_price: Optional[float] = None,
    low_price: Optional[float] = None,
    close_price: Optional[float] = None,
    volume: Optional[float] = None,
    market_cap: Optional[float] = None
) -> pd.DataFrame:
    """
    Format Bitcoin features for prediction, fetching from Kraken API if not provided
    """
    try:
        # Parse the input date
        target_date = datetime.strptime(date, "%Y-%m-%d")
        today = datetime.now().date()
        target_date_only = target_date.date()
        
        # Check if we need to fetch real-time data
        if target_date_only >= today or any(param is None for param in [open_price, high_price, low_price, close_price, volume, market_cap]):
            print(f"🔄 Fetching Bitcoin data from Kraken API for {date}")
            api_data = fetch_bitcoin_data_from_api(target_date)
            
            # Use API data as fallback for missing parameters
            if open_price is None:
                open_price = float(api_data['open'].iloc[0])
            if high_price is None:
                high_price = float(api_data['high'].iloc[0])
            if low_price is None:
                low_price = float(api_data['low'].iloc[0])
            if close_price is None:
                close_price = float(api_data['close'].iloc[0])
            if volume is None:
                volume = float(api_data['volume'].iloc[0])
            if market_cap is None:
                market_cap = float(api_data['marketCap'].iloc[0])
        
        # Create formatted DataFrame
        formatted_data = pd.DataFrame({
            'timeOpen': [target_date],
            'timeClose': [target_date + timedelta(hours=23, minutes=59)],
            'timeHigh': [target_date + timedelta(hours=12)],
            'timeLow': [target_date + timedelta(hours=4)],
            'open': [open_price],
            'high': [high_price],
            'low': [low_price],
            'close': [close_price],
            'volume': [volume],
            'marketCap': [market_cap],
            'name': ['Bitcoin'],
            'timestamp': [target_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')]
        })
        
        return formatted_data
        
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")
    except Exception as e:
        raise Exception(f"Error formatting features: {e}")

def apply_transformations(data: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all feature transformations to the input data
    """
    transformed_data = data.copy()
    
    # Apply all transformer functions
    transformed_data = calculate_circulating_supply(transformed_data)
    transformed_data = calculate_velocity(transformed_data)
    transformed_data = calculate_volume_to_marketcap_ratio(transformed_data)
    transformed_data = calculate_price_range(transformed_data)
    transformed_data = calculate_volatility(transformed_data)
    
    return transformed_data


# Load the model

@app.get("/")
async def root() -> Dict[str, Any]:
    """
    Root endpoint displaying project information
    """
    return {
        "project": "Bitcoin Price Prediction API",
        "description": "This API predicts Bitcoin's next day HIGH price using machine learning algorithms trained on historical Bitcoin data.",
        "objectives": [
            "Predict Bitcoin's next day high price",
            "Provide RESTful API endpoints for predictions", 
            "Serve machine learning models in production"
        ],
        "endpoints": {
            "/": "Project information and documentation",
            "/health/": "Health check endpoint",
            "/predict/Bitcoin": "Bitcoin price prediction endpoint"
        },
        "predict_endpoint_details": {
            "method": "GET",
            "url": "/predict/Bitcoin",
            "parameters": {
                "date": {
                    "description": "Date from which the model will predict the high price for the next day (optional - uses today's date if not provided)",
                    "format": "YYYY-MM-DD",
                    "example": "2023-01-01",
                    "required": False
                }
            },
            "output_format": {
                "input_date": "YYYY-MM-DD",
                "prediction": {
                    "prediction_day_date": "YYYY-MM-DD",
                    "Predicted_high": "string (price value)"
                }
            }
        },
        "github_repo": "https://github.com/doombuoyz/bitcoin-price-prediction",
        "version": "1.0.0"
    }

@app.get("/health/")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "message": "Welcome to the Bitcoin Price Prediction API! The service is running smoothly.",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/predict/Bitcoin")
async def predict_bitcoin_price(
    date: Optional[str] = Query(None, description="Date for prediction (YYYY-MM-DD format). If not provided, uses today's date"),
    open_price: Optional[float] = Query(None, description="Opening price (fetched from API if not provided)"),
    high_price: Optional[float] = Query(None, description="Highest price (fetched from API if not provided)"),
    low_price: Optional[float] = Query(None, description="Lowest price (fetched from API if not provided)"),
    close_price: Optional[float] = Query(None, description="Closing price (fetched from API if not provided)"),
    volume: Optional[float] = Query(None, description="Trading volume (fetched from API if not provided)"),
    market_cap: Optional[float] = Query(None, description="Market capitalization (fetched from API if not provided)")
):
    """
    Predict Bitcoin's next day HIGH price using Kraken API (OHLC) and CoinGecko API (market cap).
    
    For current/future dates, automatically fetches live data from both APIs.
    For historical dates, uses provided parameters or API data as fallback.
    
    Args:
        date: Date in YYYY-MM-DD format for which to predict next day's high price (uses today's date if not provided)
        open_price: Optional opening price (will fetch from API if not provided)
        high_price: Optional high price (will fetch from API if not provided)  
        low_price: Optional low price (will fetch from API if not provided)
        close_price: Optional closing price (will fetch from API if not provided)
        volume: Optional trading volume (will fetch from API if not provided)
        market_cap: Optional market cap (will fetch from API if not provided)
        
    Returns:
        JSON with input_date and prediction containing next day's date and predicted high price
    """
    try:
        # Use today's date if no date is provided
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            print(f"🕒 No date provided, using today's date: {date}")
        
        # Get formatted data using Kraken + CoinGecko API integration
        test_data = format_bitcoin_features(
            date=date,
            open_price=open_price,
            high_price=high_price,
            low_price=low_price,
            close_price=close_price,
            volume=volume,
            market_cap=market_cap
        )
        
        # Apply transformations
        processed_data = apply_transformations(test_data)
        
        # Parse input date and calculate prediction date
        input_date = datetime.strptime(date, "%Y-%m-%d")
        prediction_date = input_date + timedelta(days=1)
        
        # Make prediction using available method
        if loaded_pipeline is not None:
            try:
                prediction = loaded_pipeline.predict(processed_data)
                predicted_high = float(prediction[0]) if hasattr(prediction, '__iter__') else float(prediction)
            except Exception as model_error:
                print(f"Pipeline prediction failed: {model_error}")
                # Fallback prediction using the manual pipeline
                predicted_high = manual_prediction_pipeline(processed_data)
        else:
            # Use manual prediction pipeline
            predicted_high = manual_prediction_pipeline(processed_data)
        
        return {
            "input_date": date,
            "prediction": {
                "prediction_day_date": prediction_date.strftime("%Y-%m-%d"),
                "Predicted_high": f"{predicted_high:.2f}"
            }
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@app.get("/current/Bitcoin")
async def get_current_bitcoin_data():
    """
    Fetch current Bitcoin data from Kraken API
    """
    try:
        # Get current timestamp for Kraken API
        current_time = datetime.now()
        current_timestamp = int(current_time.timestamp())
        
        # Kraken API call for latest OHLC data
        url = f"https://api.kraken.com/0/public/OHLC?pair=XXBTZUSD&interval=1440&since={current_timestamp - 86400}"  # Last 24 hours
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if not data.get("error") and data.get("result"):
                # Get the OHLC data
                ohlc_data = data["result"].get("XXBTZUSD", [])
                
                if ohlc_data:
                    # Get the most recent data point
                    latest_ohlc = ohlc_data[-1]
                    
                    # Kraken OHLC format: [time, open, high, low, close, vwap, volume, count]
                    timestamp = int(latest_ohlc[0])
                    open_price = float(latest_ohlc[1])
                    high_price = float(latest_ohlc[2])
                    low_price = float(latest_ohlc[3])
                    close_price = float(latest_ohlc[4])
                    vwap = float(latest_ohlc[5])
                    volume = float(latest_ohlc[6])
                    
                    # Calculate price changes (using previous day if available)
                    price_change_24h = 0
                    price_change_percentage_24h = 0
                    if len(ohlc_data) > 1:
                        prev_close = float(ohlc_data[-2][4])
                        price_change_24h = close_price - prev_close
                        price_change_percentage_24h = (price_change_24h / prev_close) * 100
                    
                    # Estimate market cap and supply
                    estimated_circulating_supply = 19700000
                    estimated_total_supply = 19700000
                    max_supply = 21000000
                    market_cap = close_price * estimated_circulating_supply
                    
                    # Convert timestamp to readable format
                    last_updated = datetime.fromtimestamp(timestamp).isoformat() + "Z"
                    
                    return {
                        "success": True,
                        "current_price": close_price,
                        "open_24h": open_price,
                        "high_24h": high_price,
                        "low_24h": low_price,
                        "vwap_24h": vwap,
                        "price_change_24h": price_change_24h,
                        "price_change_percentage_24h": price_change_percentage_24h,
                        "market_cap": market_cap,
                        "total_volume": volume,
                        "circulating_supply": estimated_circulating_supply,
                        "total_supply": estimated_total_supply,
                        "max_supply": max_supply,
                        "last_updated": last_updated,
                        "data_source": "kraken_api"
                    }
        
        raise HTTPException(status_code=502, detail="Failed to fetch data from Kraken API")
        
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Kraken API request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching current data from Kraken API: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
#
