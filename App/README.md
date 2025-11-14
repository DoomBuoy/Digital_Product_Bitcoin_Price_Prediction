# Crypto Dashboard - Streamlit Application

A modern, interactive cryptocurrency dashboard built with Streamlit that allows users to track crypto prices, analyze trends, and customize the application theme.

## Contributors

- Agam Singh Saini

## Features

### 🎨 Theme Customization
- Upload custom Streamlit theme files (.toml)
- Manual theme configuration with color pickers
- Pre-built theme options (Dark, Light, Neon, Crypto)
- Real-time theme application

### 📊 Crypto Dashboard
- **Landing Page**: Overview of top cryptocurrencies
- **Real-time Data**: Live prices and 24h price changes
- **Market Metrics**: Market cap, volume, and rankings
- **Interactive Selection**: Click to view detailed crypto information

### 🔍 Detailed Crypto Analysis
- **Price History**: Interactive charts with multiple timeframes (7d, 30d, 90d, 1y)
- **Key Statistics**: All-time high/low, circulating supply, max supply
- **Market Data**: Volume, market cap, and market ranking
- **Descriptions**: Detailed information about each cryptocurrency

## Installation

### Option 1: Local Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   poetry run streamlit run app/main.py
   ```

### Option 2: Using Docker

1. **Build the Docker image:**
   ```bash
   docker build -t crypto-dashboard .
   ```

2. **Run the application:**
   ```bash
   docker run -p 8501:8501 crypto-dashboard
   ```

3. **Access the app at:** `http://localhost:8501`

## Deployment

### Docker Deployment

The application includes a Dockerfile for containerized deployment:

- **Base Image**: Python 3.11.4 slim
- **Port**: 8501
- **Command**: `streamlit run app/main.py`

#### Prerequisites
- Docker must be installed on your system. Download from [docker.com](https://www.docker.com/get-started) if needed.
- Ensure you're in the project root directory (`AT3_Group2_Streamlit_Application`).

#### Steps to Create and Run the Docker Container

1. **Build the Docker Image**
   ```bash
   docker build -t crypto-dashboard .
   ```
   - This builds a Docker image named `crypto-dashboard` using the Dockerfile.
   - The build process installs dependencies and copies your application code.

2. **Run the Docker Container**
   ```bash
   docker run -p 8501:8501 crypto-dashboard
   ```
   - `-p 8501:8501` maps port 8501 from the container to your host machine.
   - The container starts the Streamlit application automatically.

3. **Access the Application**
   - Open your web browser and navigate to: `http://localhost:8501`
   - You should see your crypto dashboard running.

4. **Stop the Container** (when done)
   - Press `Ctrl+C` in the terminal, or run `docker stop <container_id>` (find ID with `docker ps`).

#### Additional Docker Commands
- **View running containers:** `docker ps`
- **View all containers:** `docker ps -a`
- **Remove a container:** `docker rm <container_id>`
- **Remove an image:** `docker rmi crypto-dashboard`
- **Run in detached mode:** `docker run -d -p 8501:8501 crypto-dashboard`

#### Troubleshooting
- If port 8501 is in use, change mapping: `docker run -p 8502:8501 crypto-dashboard` (access at localhost:8502)
- Ensure Docker Desktop is running (on Windows/Mac)
- Check terminal output for build errors

### Local Development

For development, use Poetry or pip as described in Installation.

## Customization

### Adding New Themes
Create a new `.toml` file in the `themes/` folder with the following structure:

```toml
[theme]
primaryColor = "#YOUR_COLOR"
backgroundColor = "#YOUR_COLOR"
secondaryBackgroundColor = "#YOUR_COLOR"
textColor = "#YOUR_COLOR"
font = "sans serif"  # or "serif" or "monospace"

[server]
enableCORS = false
enableXsrfProtection = false
```

### Adding New Cryptocurrencies
The application automatically fetches the top 50 cryptocurrencies from CoinGecko. To modify this:
1. Edit the `get_crypto_list()` function in `main.py`
2. Adjust the `per_page` parameter for more/fewer cryptos
3. Modify the `order` parameter to change sorting criteria

## Usage

### 1. Theme Configuration
- Use the sidebar to upload a custom theme file or manually adjust colors
- Sample theme files are provided in the `themes/` folder
- Apply changes and refresh to see the new theme

### 2. Crypto Exploration
- Browse the landing page to see top cryptocurrencies
- Click on any crypto card to view detailed analysis
- Use the time period selector to view different chart timeframes
- Navigate back to the landing page using the back button

## File Structure

```
AT3_Group2_Streamlit_Application/
├── app/
│   ├── main.py                 # Main Streamlit application
│   ├── pages.py                # Landing page logic
│   ├── crypto_data.py          # Cryptocurrency data fetching
│   ├── st_theme.py             # Theme application functions
│   └── __pycache__/
├── coin/
│   ├── bitcoin.py       # Bitcoin detail page
│   └── __pycache__/
├── themes/                     # Sample theme files
│   ├── dark_theme.toml
│   ├── light_theme.toml
│   ├── neon_theme.toml
│   ├── crypto_theme.toml
│   └── README.md
├── Dockerfile                  # Docker configuration
├── pyproject.toml              # Poetry project configuration
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── github.txt                  # GitHub repository info
```

## Dependencies

- **streamlit**: Web application framework
- **requests**: HTTP library for API calls
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive plotting library
- **yfinance**: Financial data from Yahoo Finance

## Data Sources

- **CoinGecko API**: Real-time cryptocurrency data
- **Yahoo Finance**: Historical price data (fallback)
- **Fallback Data**: Sample data when APIs are unavailable

## Features in Detail

### Theme System
The application supports dynamic theme switching through:
- File upload functionality for `.toml` theme files
- Manual color picker interface
- Predefined theme templates
- Real-time theme preview

### Navigation System
- Session state management for page routing
- Smooth transitions between landing and detail pages
- Persistent crypto selection across page reloads

### Data Caching
- 5-minute cache for cryptocurrency list
- 10-minute cache for historical price data
- Automatic fallback data when APIs are unavailable

## Deployment

### Docker Deployment

The application includes a Dockerfile for containerized deployment:

- **Base Image**: Python 3.11.4 slim
- **Port**: 8501
- **Command**: `streamlit run app/main.py`

To deploy using Docker:

1. Build the image: `docker build -t crypto-dashboard .`
2. Run the container: `docker run -p 8501:8501 crypto-dashboard`
3. Access at `http://localhost:8501`

### Local Development

For development, use Poetry or pip as described in Installation.

## Troubleshooting

### API Issues
If cryptocurrency data isn't loading:
- Check your internet connection
- The app will automatically use fallback sample data
- API rate limits may apply for frequent requests

### Theme Not Applying
- Ensure the theme file is valid TOML format
- Refresh the page after applying theme changes
- Check that all required theme properties are present

### Performance Issues
- The app uses caching to improve performance
- Large datasets may take longer to load
- Consider reducing the number of displayed cryptocurrencies

## License

This project is for educational purposes as part of the MDSI AMLA Assignment 3.