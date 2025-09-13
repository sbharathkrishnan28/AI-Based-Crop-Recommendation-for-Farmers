# utils/config.py
import os

# Data paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CROP_DATA_PATH = os.path.join(DATA_DIR, 'crop_data.csv')
MARKET_DATA_PATH = os.path.join(DATA_DIR, 'market_data.csv')

# Model paths
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# API settings
API_HOST = '0.0.0.0'
API_PORT = 5000
DEBUG = True

# Model training parameters
TRAIN_TEST_SPLIT = 0.2
RANDOM_STATE = 42
FORECAST_DAYS = 30