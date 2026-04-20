# 🪙 Bitcoin Price Prediction API

A production-ready FastAPI-based REST API for predicting Bitcoin's next day HIGH price using machine learning algorithms trained on historical Bitcoin data. This API features robust error handling, automatic fallback systems, and comprehensive Docker deployment capabilities.

## 🎯 Project Objectives

- **Predict Bitcoin's Next Day High Price** using advanced machine learning algorithms
- **Provide RESTful API Endpoints** for real-time Bitcoin price predictions
- **Serve ML Models in Production** with robust error handling and fallback systems
- **Enable Easy Integration** with other applications and services
- **Support Container Deployment** via Docker and Docker Hub
- **Maintain High Availability** with health monitoring and comprehensive testing
- **Integrate Multiple Data Sources** using Kraken API (OHLC) and CoinGecko API (market cap)
- **Provide Real-time Market Data** with current Bitcoin statistics and price changes

## 🚀 Features

- **🔮 Real-time Predictions**: Get Bitcoin price predictions for any date using ML models
- **🌐 RESTful API**: Clean, well-documented FastAPI endpoints with automatic OpenAPI docs
- **💚 Health Monitoring**: Built-in health check endpoint for system monitoring
- **🛡️ Robust Error Handling**: Comprehensive error responses, validation, and automatic fallbacks
- **🐳 Docker Support**: Full containerization with Docker Hub deployment ready
- **📊 Smart Fallback System**: Manual prediction pipeline when model loading fails
- **🧪 Comprehensive Testing**: Automated test suite for all endpoints and scenarios
- **📚 Interactive Documentation**: Auto-generated API docs at `/docs` and `/redoc`
- **🔧 Model Flexibility**: Supports both joblib pipeline and manual transformer functions
- **📅 Optional Date Parameter**: Automatically uses today's date when not specified
- **🔗 Dual API Integration**: Combines Kraken API (OHLC data) and CoinGecko API (market cap)
- **📈 Current Market Data**: Real-time Bitcoin data endpoint with 24h price changes
- **🔄 Automatic Data Fetching**: Smart API calls for current/future dates with fallback support

## 📋 Requirements

- **Python 3.11.4** (exact version for compatibility)
- **Poetry** (for dependency management and virtual environments)
- **Docker Desktop** (optional, for containerized deployment)
- **Git** (for version control and cloning)
- **Docker Hub Account** (optional, for public deployment)

## 🛠️ Installation

### Option 1: Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Doombuoyz/API_Bitcoin.git
   cd API_Bitcoin
   ```

2. **Install Poetry** (if not already installed)
   ```bash
   # Windows (PowerShell)
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   
   # macOS/Linux
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies using Poetry**
   ```bash
   poetry install
   ```

4. **Verify model file location**
   - Ensure `models/bitcoin_prediction_pipeline.joblib` exists
   - If missing, the API will use the fallback prediction system

### Option 2: Docker Deployment

1. **Pull from Docker Hub** (if available)
   ```bash
   docker pull doombuoyz/bitcoin-prediction-api:latest
   docker run -p 8000:8000 doombuoyz/bitcoin-prediction-api:latest
   ```

2. **Or build locally**
   ```bash
   git clone https://github.com/Doombuoyz/API_Bitcoin.git
   cd API_Bitcoin
   docker build -t bitcoin-prediction-api .
   docker run -p 8000:8000 bitcoin-prediction-api
   ```

## 🏃‍♂️ Running the Application

### 🔧 Development Mode (Recommended for Development)
```bash
# Activate Poetry environment and start development server
poetry run fastapi dev app/main.py
```
- **URL**: `http://localhost:8000`
- **Features**: Auto-reload on file changes, debug mode enabled
- **Best for**: Development, testing, debugging

### 🚀 Production Mode
```bash
# Run with Uvicorn for production
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```
- **Features**: Multiple workers, optimized performance
- **Best for**: Production deployment, high traffic

### 🐳 Docker Deployment
```bash
# Option 1: Use Docker Compose (recommended)
docker build -t bitcoin-prediction-api .
docker run -d --name bitcoin-api -p 8000:8000 bitcoin-prediction-api

# Option 2: Use the deployment notebook
# Open Bitcoin_API_Docker_Deployment.ipynb and run all cells

# Option 3: Pull from Docker Hub
docker pull doombuoyz/bitcoin-prediction-api:latest
docker run -p 8000:8000 doombuoyz/bitcoin-prediction-api:latest
```

### 🧪 Testing Mode
```bash
# Start the server in one terminal
poetry run fastapi dev app/main.py

# Run tests in another terminal
python test.py
# or
python test_model_loading.py
```

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

## 🔗 API Endpoints

### 1. Root Endpoint
- **URL**: `/`
- **Method**: GET
- **Description**: Project information and documentation
- **Response**: JSON with project details, endpoints, and usage information

### 2. Health Check
- **URL**: `/health/`
- **Method**: GET
- **Description**: Service health status
- **Response**:
  ```json
  {
    "status": "healthy",
    "message": "Welcome to the Bitcoin Price Prediction API! The service is running smoothly.",
    "timestamp": "2023-01-01T12:00:00"
  }
  ```

### 3. Bitcoin Price Prediction
- **URL**: `/predict/Bitcoin`
- **Method**: GET
- **Description**: Predict Bitcoin's next day HIGH price using Kraken API (OHLC) and CoinGecko API (market cap)
- **Parameters**:
  - `date` (optional): Date in YYYY-MM-DD format (uses today's date if not provided)
  - `open_price` (optional): Opening price (fetched from API if not provided)
  - `high_price` (optional): Highest price (fetched from API if not provided)
  - `low_price` (optional): Lowest price (fetched from API if not provided)
  - `close_price` (optional): Closing price (fetched from API if not provided)
  - `volume` (optional): Trading volume (fetched from API if not provided)
  - `market_cap` (optional): Market capitalization (fetched from API if not provided)
- **Example Requests**:
  ```
  # Using today's date automatically
  GET /predict/Bitcoin

  # Using specific date
  GET /predict/Bitcoin?date=2023-01-01

  # Using custom parameters
  GET /predict/Bitcoin?date=2023-01-01&close_price=30000&volume=50000
  ```
- **Example Response**:
  ```json
  {
    "input_date": "2023-01-01",
    "prediction": {
      "prediction_day_date": "2023-01-02",
      "Predicted_high": "31200.50"
    }
  }
  ```

### 4. Current Bitcoin Data
- **URL**: `/current/Bitcoin`
- **Method**: GET
- **Description**: Fetch current Bitcoin market data from Kraken API
- **Response**: Real-time Bitcoin data including prices, volume, market cap, and 24h changes
- **Example Response**:
  ```json
  {
    "success": true,
    "current_price": 67000.25,
    "open_24h": 66500.00,
    "high_24h": 67500.50,
    "low_24h": 66000.00,
    "vwap_24h": 66800.30,
    "price_change_24h": 500.25,
    "price_change_percentage_24h": 0.75,
    "market_cap": 1314000000000,
    "total_volume": 28500.5,
    "circulating_supply": 19700000,
    "total_supply": 19700000,
    "max_supply": 21000000,
    "last_updated": "2023-01-01T12:00:00Z",
    "data_source": "kraken_api"
  }
  ```

## 🧪 Testing

### Comprehensive Test Suite

**Main API Tests** (`test.py`):
```bash
# Start the API server first
poetry run fastapi dev app/main.py

# In another terminal, run comprehensive tests
python test.py
```


```

**API Integration Tests**:
```bash


# Test CoinGecko API integration

python test_coingecko_api.py


```

### Test Coverage Includes:
- ✅ **Root Endpoint** (`/`) - Project information and documentation
- ✅ **Health Check** (`/health/`) - Service status verification  
- ✅ **Prediction Endpoint** (`/predict/Bitcoin`) - Bitcoin price predictions with optional date
- ✅ **Current Data Endpoint** (`/current/Bitcoin`) - Real-time Bitcoin data from Kraken API
- ✅ **Dual API Integration** - Kraken (OHLC) + CoinGecko (market cap) data fetching
- ✅ **Error Handling** - Invalid date formats, missing parameters, API failures
- ✅ **Model Loading** - Both successful and fallback scenarios
- ✅ **Multiple Predictions** - Different dates, custom parameters, and edge cases
- ✅ **Docker Container** - Container health and API accessibility

### Manual Testing URLs:
Once the server is running, test these endpoints in your browser:
- 🏠 **Main**: http://localhost:8000
- 💚 **Health**: http://localhost:8000/health/
- 📈 **Prediction (auto date)**: http://localhost:8000/predict/Bitcoin
- 📈 **Prediction (specific date)**: http://localhost:8000/predict/Bitcoin?date=2023-01-15
- 📊 **Current Data**: http://localhost:8000/current/Bitcoin
- 📚 **Documentation**: http://localhost:8000/docs
- 📖 **Alternative Docs**: http://localhost:8000/redoc

## 📁 Project Structure

```
API_Bitcoin/                                    # 🏠 Project Root
├── 📱 app/
│   └── main.py                                # 🚀 FastAPI application with all endpoints
├── 🤖 models/
│   ├── .gitkeep                              # 📝 Git placeholder
│   └── bitcoin_prediction_pipeline.joblib    # 🧠 Trained ML model
├── 📊 Bitcoin_API_Docker_Deployment.ipynb    # 🐳 Docker deployment guide
├── 🧪 test.py                                # 🔬 Comprehensive API test suite
├── 🧪 test_model_loading.py                  # 🔧 Model loading verification tests
├── 🧪 test_kraken_api.py                     # 🌐 Kraken API integration tests
├── 🧪 test_coingecko_api.py                  # � CoinGecko API integration tests
├── 🧪 test_feature_pipeline.py               # 🔬 Feature engineering pipeline tests
├── 🧪 demo_optional_date.py                  # 📅 Demo script for optional date functionality
├── 🧪 test_optional_date.py                  # 🧪 Test script for optional date parameter
├── �📋 requirements.txt                        # 📦 Docker dependencies
├── 🐳 Dockerfile                             # 🏗️ Container configuration
├── 🚫 .dockerignore                          # 🙈 Docker build exclusions
├── ⚙️ pyproject.toml                         # 📋 Poetry project configuration
├── 🔒 poetry.lock                            # 🔐 Locked dependency versions
└── 📚 README.md                              # 📖 This documentation
```

### Key Files Explained:
- **`app/main.py`**: Complete FastAPI application with dual API integration (Kraken + CoinGecko)
- **`models/bitcoin_prediction_pipeline.joblib`**: Pre-trained ML model (with fallback support)
- **`test_kraken_api.py`**: Tests for Kraken API OHLC data fetching
- **`test_coingecko_api.py`**: Tests for CoinGecko API market cap data fetching
- **`test_feature_pipeline.py`**: Tests for feature engineering pipeline
- **`demo_optional_date.py`**: Demonstration of optional date parameter functionality
- **`Bitcoin_API_Docker_Deployment.ipynb`**: Step-by-step Docker Hub deployment notebook
- **`test.py`**: Production-ready test suite for all API endpoints
- **`test_model_loading.py`**: Specialized tests for model loading scenarios

## 🔧 Model Information

The API uses a pre-trained machine learning pipeline that includes:
- Feature engineering (circulating supply, velocity, EMA calculations)
- Log transformations for numerical stability
- Cyclical encoding for temporal features
- Feature normalization and selection
- Trained model for next-day high price prediction

### Input Features Used:
- `open`, `high`, `low`, `close` prices
- `volume` and `marketCap`
- `timeOpen` (for temporal features)
- Derived features: circulating supply, velocity, EMA

### Model Pipeline:
1. Calculate circulating supply
2. Calculate velocity metrics
3. Compute 12-day EMA
4. Apply log transformations
5. Extract cyclical day-of-week features
6. Normalize numerical features
7. Select final feature set
8. Make prediction

### API Integration:
The API integrates with two external data sources for real-time data:
- **Kraken API**: Provides OHLC (Open, High, Low, Close) price data and volume
- **CoinGecko API**: Provides historical market capitalization data
- **Fallback System**: Uses estimated values if APIs are unavailable
- **Smart Data Fetching**: Automatically fetches real-time data for current/future dates

## 🐳 Docker Deployment

### 📓 Interactive Deployment Guide
Use the **`Bitcoin_API_Docker_Deployment.ipynb`** notebook for step-by-step deployment:

1. Open the notebook in Jupyter/VS Code
2. Replace `doombuoyz` with your Docker Hub username
3. Run all cells in order
4. Your API will be deployed to Docker Hub automatically!

### 🚀 Quick Docker Commands

```bash
# Build image locally
docker build --no-cache -t bitcoin-prediction-api .

# Run container locally  
docker run -d --name bitcoin-api -p 8000:8000 bitcoin-prediction-api

# Check container logs
docker logs bitcoin-api

# Stop and cleanup
docker stop bitcoin-api && docker rm bitcoin-api
```

### 🌐 Docker Hub Deployment

```bash
# Tag for Docker Hub (replace 'yourusername')
docker tag bitcoin-prediction-api yourusername/bitcoin-prediction-api:latest

# Push to Docker Hub
docker push yourusername/bitcoin-prediction-api:latest

# Others can now use your API:
docker pull yourusername/bitcoin-prediction-api:latest
docker run -p 8000:8000 yourusername/bitcoin-prediction-api:latest
```

### 🔧 Docker Features
- **Multi-stage Build**: Optimized image size and security
- **Health Checks**: Built-in container health monitoring  
- **Non-root User**: Enhanced security practices
- **Poetry Integration**: Proper dependency management
- **Environment Variables**: Configurable runtime settings

## 🚨 Error Handling & Reliability

### 🛡️ Comprehensive Error Management
- **400 Bad Request**: Invalid date format (YYYY-MM-DD required)
- **422 Validation Error**: Missing or invalid query parameters
- **500 Internal Server Error**: Model loading issues with automatic fallback
- **Custom Exception Handling**: Detailed error messages and debugging info

### 🔄 Automatic Fallback System
The API features a robust fallback mechanism:

1. **Primary**: Attempts to load pre-trained joblib pipeline
2. **Fallback**: Uses manual prediction pipeline if model fails to load
3. **Graceful Degradation**: API remains functional even with model issues
4. **Error Logging**: Detailed logs for debugging and monitoring

### 🧠 Model Loading Strategies
```python
# The API handles multiple scenarios:
if loaded_pipeline is not None:
    # Use trained ML model
    prediction = loaded_pipeline.predict(data)
else:
    # Use manual transformation pipeline
    prediction = manual_prediction_pipeline(data)
```

### 🔍 Troubleshooting
- **Model Loading Issues**: Check `test_model_loading.py` output
- **API Not Responding**: Verify port 8000 is available
- **Prediction Errors**: Validate date format (YYYY-MM-DD)
- **Docker Issues**: Check container logs with `docker logs bitcoin-api`

## 📊 Example Usage

### Python Client Example
```python
import requests

# Make a prediction with today's date (automatic)
response = requests.get("http://localhost:8000/predict/Bitcoin")
data = response.json()
print(f"Input Date: {data['input_date']}")
print(f"Predicted High Price: ${data['prediction']['Predicted_high']}")

# Make a prediction for specific date
response = requests.get("http://localhost:8000/predict/Bitcoin?date=2023-01-01")
data = response.json()
print(f"Input Date: {data['input_date']}")
print(f"Predicted High Price: ${data['prediction']['Predicted_high']}")

# Get current Bitcoin data
response = requests.get("http://localhost:8000/current/Bitcoin")
current_data = response.json()
print(f"Current Price: ${current_data['current_price']}")
print(f"24h Change: {current_data['price_change_percentage_24h']}%")
```

### cURL Examples
```bash
# Health check
curl -X GET "http://localhost:8000/health/"

# Make prediction with today's date
curl -X GET "http://localhost:8000/predict/Bitcoin"

# Make prediction for specific date
curl -X GET "http://localhost:8000/predict/Bitcoin?date=2023-01-01"

# Get current Bitcoin data
curl -X GET "http://localhost:8000/current/Bitcoin"

# Make prediction with custom parameters
curl -X GET "http://localhost:8000/predict/Bitcoin?date=2023-01-01&close_price=30000&volume=50000"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links & Resources

- **📱 GitHub Repository**: https://github.com/Doombuoyz/API_Bitcoin
- **🐳 Docker Hub Image**: https://hub.docker.com/r/doombuoyz/bitcoin-prediction-api
- **📚 API Documentation**: http://localhost:8000/docs (when running locally)
- **📖 Alternative Docs**: http://localhost:8000/redoc (when running locally)  
- **🐛 Issue Tracker**: https://github.com/Doombuoyz/API_Bitcoin/issues
- **📊 Live Demo**: (Deploy your own using the Docker deployment notebook!)

## 📞 Support & Documentation

### 🆘 Getting Help
1. **Check Interactive Docs**: Visit `/docs` endpoint for complete API reference
2. **Run Test Suite**: Execute `test.py` to verify functionality
3. **Model Loading Issues**: Use `test_model_loading.py` for diagnostics
4. **Docker Problems**: Follow `Bitcoin_API_Docker_Deployment.ipynb` step-by-step
5. **Create GitHub Issue**: Report bugs or request features

### 📋 Quick Reference
```bash
# Essential commands for development
poetry run fastapi dev app/main.py          # Start development server
python test.py                              # Run comprehensive API tests
python test_model_loading.py                # Test model loading
python test_kraken_api.py                   # Test Kraken API integration
python test_coingecko_api.py                # Test CoinGecko API integration
python test_feature_pipeline.py             # Test feature engineering
python demo_optional_date.py                # Demo optional date functionality
docker build -t bitcoin-api .               # Build Docker image
docker run -p 8000:8000 bitcoin-api         # Run Docker container
```

### 🎯 Project Status
- ✅ **API Endpoints**: 4 fully functional endpoints with comprehensive testing
- ✅ **Dual API Integration**: Kraken (OHLC) + CoinGecko (market cap) data fetching
- ✅ **Optional Date Parameter**: Automatic today's date usage when not specified
- ✅ **Model Integration**: Robust loading with automatic fallback
- ✅ **Docker Support**: Complete containerization and deployment
- ✅ **Documentation**: Interactive API docs and deployment guides
- ✅ **Error Handling**: Production-ready error management
- ✅ **Testing**: Comprehensive test coverage for all scenarios and APIs

---

**🚀 Ready to predict Bitcoin prices? Clone, run, and deploy your own instance today!** 🪙