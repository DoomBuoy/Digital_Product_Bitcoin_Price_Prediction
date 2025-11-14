# 🪙 Digital Product: Bitcoin Price Prediction System

A comprehensive cryptocurrency analytics platform featuring machine learning-powered price predictions, interactive dashboards, and production-ready APIs. This end-to-end solution combines advanced ML models, real-time data visualization, and scalable web services for Bitcoin price analysis.

## 🌟 Live Demo

**🚀 Streamlit Dashboard**: [https://digitalappuctbitcoinpriceprediction-8f9newvrhuqkth7wb25e7l.streamlit.app/](https://digitalappuctbitcoinpriceprediction-8f9newvrhuqkth7wb25e7l.streamlit.app/)

## 📋 Project Overview

This digital product delivers a complete Bitcoin price prediction ecosystem with three integrated components:

### 🤖 ML Model (`ML_Model/`)
- **Advanced ML Pipeline**: XGBoost, LightGBM, CatBoost with hyperparameter optimization
- **Data Processing**: Automated Bitcoin data collection (2015-2025) from multiple sources
- **Model Training**: Feature engineering, cross-validation, and experiment tracking with Weights & Biases
- **Interpretability**: LIME explanations for model predictions
- **Performance**: 99.14% R² Score on historical data

### 🚀 Prediction API (`API_Bitcoin/`)
- **FastAPI Backend**: RESTful API for real-time Bitcoin price predictions
- **Dual Data Sources**: Kraken API (OHLC data) + CoinGecko API (market cap)
- **Production Ready**: Docker deployment, health monitoring, error handling
- **Smart Fallbacks**: Automatic fallback when model loading fails
- **Interactive Docs**: Auto-generated API documentation at `/docs`

### 📊 Streamlit Dashboard (`App/`)
- **Interactive UI**: Modern crypto dashboard with theme customization
- **Real-time Data**: Live Bitcoin prices, market metrics, and price history charts
- **Multi-timeframe Analysis**: 7d, 30d, 90d, 1y price visualizations with Plotly
- **Theme System**: Customizable themes (Dark, Light, Neon, Crypto)
- **Responsive Design**: Mobile-friendly interface with smooth navigation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │     ML Model    │
│   Dashboard     │◄──►│   Prediction    │◄──►│   Training      │
│                 │    │     API         │    │   Pipeline      │
│ - Real-time UI  │    │                 │    │                 │
│ - Data viz      │    │ - REST endpoints│    │ - XGBoost       │
│ - Theme system  │    │ - Health checks │    │ - Feature eng   │
└─────────────────┘    │ - Docker deploy │    │ - W&B tracking  │
                       └─────────────────┘    └─────────────────┘
                              ▲
                              │
                       ┌─────────────────┐
                       │   Data Sources  │
                       │                 │
                       │ - Kraken API    │
                       │ - CoinGecko API │
                       │ - Yahoo Finance │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11.4
- Poetry (for dependency management)
- Docker (optional, for containerized deployment)

### 1. Clone the Repository
```bash
git clone https://github.com/DoomBuoy/Digital_Product_Bitcoin_Price_Prediction.git
cd Digital_Product_Bitcoin_Price_Prediction
```

### 2. Start the Prediction API
```bash
cd API_Bitcoin
poetry install
poetry run fastapi dev app/main.py
```
API will be available at: http://localhost:8000

### 3. Launch the Dashboard
```bash
cd ../App
pip install -r requirements.txt
streamlit run app/main.py
```
Dashboard will be available at: http://localhost:8501

### 4. Explore ML Experiments (Optional)
```bash
cd ../ML_Model
poetry install
poetry run jupyter lab
```

## 📊 Key Features

### 🔮 ML-Powered Predictions
- **Next-Day High Price**: Predict Bitcoin's next day high using trained ML models
- **Real-time Data**: Live OHLC data from Kraken API + market cap from CoinGecko
- **Feature Engineering**: Circulating supply, velocity metrics, EMA calculations
- **Model Interpretability**: LIME explanations for prediction transparency

### 📈 Interactive Analytics
- **Price History Charts**: Interactive Plotly visualizations across multiple timeframes
- **Market Metrics**: Real-time market cap, volume, 24h changes
- **Theme Customization**: Upload custom themes or use pre-built options
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### 🛡️ Production-Ready API
- **RESTful Endpoints**: Clean API design with automatic OpenAPI documentation
- **Error Handling**: Comprehensive error responses and automatic fallbacks
- **Health Monitoring**: Built-in health checks and system monitoring
- **Docker Deployment**: Containerized deployment with multi-stage builds

## 🧪 Testing & Validation

### API Testing
```bash
cd API_Bitcoin
python test.py                    # Comprehensive API tests
python test_model_loading.py      # Model loading verification
python test_kraken_api.py         # Kraken API integration
python test_coingecko_api.py      # CoinGecko API integration
```

### Dashboard Testing
```bash
cd App
streamlit run app/main.py --server.headless true
```

### ML Pipeline Testing
```bash
cd ML_Model
poetry run python -m pytest
```

## 🐳 Docker Deployment

### API Deployment
```bash
cd API_Bitcoin
docker build -t bitcoin-prediction-api .
docker run -p 8000:8000 bitcoin-prediction-api
```

### Dashboard Deployment
```bash
cd App
docker build -t crypto-dashboard .
docker run -p 8501:8501 crypto-dashboard
```

## 📚 API Endpoints

### Prediction Endpoints
- `GET /predict/Bitcoin` - Predict next-day high price
- `GET /current/Bitcoin` - Get current Bitcoin data
- `GET /health/` - Health check

### Documentation
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
export API_HOST=0.0.0.0
export API_PORT=8000

# Dashboard Configuration
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Model Configuration
- Pre-trained model: `models/bitcoin_prediction_pipeline.joblib`
- Feature pipeline includes log transformations, cyclical encoding, and normalization
- Automatic fallback to manual prediction if model loading fails

## 📁 Project Structure

```
Digital_Product_Bitcoin_Price_Prediction/
├── 📁 API_Bitcoin/              # 🚀 FastAPI Prediction Service
│   ├── app/main.py             # API endpoints
│   ├── models/                 # Trained ML models
│   ├── tests/                  # API test suite
│   └── Dockerfile              # API containerization
├── 📁 App/                     # 📊 Streamlit Dashboard
│   ├── app/main.py            # Dashboard application
│   ├── themes/                # Custom themes
│   ├── requirements.txt       # Dashboard dependencies
│   └── Dockerfile             # Dashboard containerization
├── 📁 ML_Model/                # 🤖 ML Training Pipeline
│   ├── ml_model/              # Source code
│   ├── notebooks/             # Experiment notebooks
│   ├── data/                  # Training data
│   └── models/                # Model artifacts
└── README.md                  # 📖 This documentation
```

## 🛠️ Technologies Used

### Core Technologies
- **Python 3.11.4**: Primary programming language
- **FastAPI**: High-performance API framework
- **Streamlit**: Interactive web application framework
- **Poetry**: Dependency management and packaging

### ML & Data Science
- **XGBoost/LightGBM/CatBoost**: Ensemble learning algorithms
- **Hyperopt**: Hyperparameter optimization
- **LIME**: Model interpretability
- **Weights & Biases**: Experiment tracking
- **Pandas/NumPy**: Data manipulation
- **Scikit-learn**: ML utilities

### Data Visualization
- **Plotly**: Interactive charts and graphs
- **Streamlit**: Dashboard components
- **Matplotlib/Seaborn**: Static visualizations

### Infrastructure
- **Docker**: Containerization
- **Poetry**: Python packaging
- **Jupyter**: Interactive development
- **Git**: Version control

## 📊 Data Sources

### Primary Data Sources
- **Kraken API**: Real-time OHLC (Open, High, Low, Close) price data
- **CoinGecko API**: Historical market capitalization and metadata
- **Yahoo Finance**: Alternative price data source (fallback)

### Data Pipeline
- **Automated Collection**: Historical data from 2015-2025
- **Real-time Updates**: Live price feeds for current predictions
- **Data Validation**: Quality checks and error handling
- **Caching**: Optimized data fetching with intelligent caching

## 🔍 Model Performance

### Key Metrics
- **R² Score**: 99.14% on validation data
- **Prediction Accuracy**: High accuracy for next-day high price predictions
- **Feature Importance**: Clear interpretability with LIME
- **Robustness**: Handles missing data and API failures gracefully

### Model Features
- **Input Features**: OHLC prices, volume, market cap, temporal features
- **Transformations**: Log scaling, cyclical encoding, EMA calculations
- **Output**: Next-day high price prediction with confidence intervals

## 🚨 Troubleshooting

### Common Issues

#### API Not Starting
```bash
# Check if port 8000 is available
netstat -an | grep 8000

# Kill conflicting processes
# On Linux/Mac: lsof -ti:8000 | xargs kill -9
# On Windows: netstat -ano | findstr :8000
```

#### Dashboard Not Loading
```bash
# Clear Streamlit cache
streamlit cache clear

# Check requirements installation
pip install -r requirements.txt
```

#### Model Loading Issues
```bash
# Verify model file exists
ls -la models/bitcoin_prediction_pipeline.joblib

# Test model loading
python -c "import joblib; joblib.load('models/bitcoin_prediction_pipeline.joblib')"
```

#### Docker Issues
```bash
# Check Docker is running
docker --version

# View container logs
docker logs <container_name>

# Clean up containers
docker system prune
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive tests for new features
- Update documentation for API changes
- Use Poetry for dependency management
- Test Docker builds locally

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Agam Singh Saini** - *Lead Developer* - [GitHub](https://github.com/DoomBuoy)

## 🙏 Acknowledgments

- **Cookiecutter Data Science** for the ML project template
- **FastAPI** and **Streamlit** communities for excellent documentation
- **CoinGecko** and **Kraken** for providing cryptocurrency data APIs
- **Weights & Biases** for experiment tracking capabilities
- **Docker** for containerization technology

## 🔗 Links & Resources

- **📱 GitHub Repository**: https://github.com/DoomBuoy/Digital_Product_Bitcoin_Price_Prediction
- **🚀 Live Dashboard**: https://digitalappuctbitcoinpriceprediction-8f9newvrhuqkth7wb25e7l.streamlit.app/
- **🐳 Docker Hub**: Search for project containers
- **📚 API Documentation**: http://localhost:8000/docs (when running locally)
- **📊 ML Experiments**: Explore the `ML_Model/notebooks/` directory
- **🐛 Issue Tracker**: https://github.com/DoomBuoy/Digital_Product_Bitcoin_Price_Prediction/issues

---

**🎯 Ready to explore Bitcoin price predictions? Clone the repository and start analyzing cryptocurrency trends today!** 🪙📈</content>
<parameter name="filePath">d:\MS_DSI\GithubProjects\Digital_Product_Bitcoin_Price_Prediction\README.md