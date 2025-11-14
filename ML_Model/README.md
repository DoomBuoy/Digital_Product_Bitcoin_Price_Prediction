# AT3 Data Product ML Experiments



Cryptocurrency Price Prediction using Machine Learning

## Overview

This project implements a comprehensive machine learning pipeline for predicting Bitcoin prices. The system analyzes historical price data for Bitcoin using various machine learning algorithms to forecast future price movements.

## Features

- **Advanced ML Algorithms**: Implementation of XGBoost, LightGBM, CatBoost, and other ensemble methods
- **Hyperparameter Optimization**: Automated tuning using Hyperopt
- **Model Interpretability**: LIME explanations for model predictions
- **Experiment Tracking**: Weights & Biases integration for experiment management
- **Data Pipeline**: Automated data downloading and processing from Google Drive

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│       └── 36120-AT3/
│           └── Bitcoin/    <- Historical Bitcoin price data (2015-2025)
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│   └── bitcoin_prediction_pipeline.joblib  <- Trained Bitcoin prediction model
│
├── notebooks          <- Jupyter notebooks with ML experiments
│   
│
├── pyproject.toml     <- Project configuration file with package metadata for
│                         ml_model and configuration for tools like ruff
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│       └── experiments/  <- Experiment figures and plots
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── ml_model   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes ml_model a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling
    │   ├── __init__.py
    │   ├── predict.py          <- Code to run model inference with trained models
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

## Installation

### Prerequisites

- **Python 3.11.4** - The project requires Python 3.11.4 specifically
- **Poetry** - For dependency management and virtual environment handling
- **Git** - For cloning the repository (if applicable)

### Environment Setup

1. **Install Poetry** (if not already installed):
   ```bash
   # Using pip
   pip install poetry

   # Or using the official installer
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Clone or navigate to the project directory**:
   ```bash
   cd path/to/ml_model
   ```

3. **Install project dependencies**:
   ```bash
   poetry install
   ```

4. **Activate the Poetry environment**:
   ```bash
   poetry shell
   ```
   Or run commands directly with Poetry:
   ```bash
   poetry run <command>
   ```

5. **Verify installation**:
   ```bash
   poetry run python --version  # Should show Python 3.11.4
   poetry run python -c "import pandas, sklearn; print('Dependencies installed successfully')"
   ```

## Usage

### Quick Start

1. **Set up the environment** (follow Installation steps above)

2. **Download and process data**:
   ```bash
   poetry run python -m ml_model.dataset
   ```

3. **Explore the Jupyter notebooks**:
   ```bash
   poetry run jupyter lab
   ```
   Open any of the experiment notebooks in the `notebooks/` directory to see the ML experiments.

### Running Individual Components

#### Data Processing
```bash
# Download Bitcoin data from Google Drive
poetry run python -m ml_model.dataset
```


### Working with Notebooks

The project includes multiple experiment notebooks. To work with them:

1. **Start Jupyter Lab**:
   ```bash
   poetry run jupyter lab
   ```

2. **Navigate to the `notebooks/` directory**

3. **Open experiment notebooks**:
   - Notebooks contain various ML experiments.



### Troubleshooting

#### Common Issues

1. **Poetry environment issues**:
   ```bash
   # Remove and recreate environment
   poetry env remove python3.11.4
   poetry install
   ```

2. **Dependency conflicts**:
   ```bash
   # Clear Poetry cache
   poetry cache clear --all pypi
   poetry install
   ```

3. **Jupyter notebook kernel issues**:
   ```bash
   # Install kernel for the environment
   poetry run python -m ipykernel install --user --name=crypto-ml-env
   ```




## Experiments

The project includes multiple Jupyter notebooks documenting different machine learning experiments:

| Team Member |
|-------------|
| Agam Singh Saini |


## Model Performance

The trained Bitcoin prediction pipeline achieves competitive performance on historical data, with comprehensive evaluation metrics and model interpretability features.





## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- **Agam Singh Saini** 

## Acknowledgments

- Cookiecutter Data Science for the project template
- CoinGecko and Kraken API for Bitcoin historical data
- Various open-source ML libraries and tools

