# utils/data_loader.py
import pandas as pd
import os
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CROP_DATA_PATH, MARKET_DATA_PATH

class DataLoader:
    def __init__(self):
        self.crop_data = None
        self.market_data = None
    
    def load_crop_data(self):
        """Load crop production data"""
        try:
            self.crop_data = pd.read_csv(CROP_DATA_PATH)
            # Convert date column if exists
            if 'date' in self.crop_data.columns:
                self.crop_data['date'] = pd.to_datetime(self.crop_data['date'])
            print(f"Loaded crop data with {len(self.crop_data)} records")
            return self.crop_data
        except Exception as e:
            print(f"Error loading crop data: {e}")
            return pd.DataFrame()
    
    def load_market_data(self):
        """Load market price data"""
        try:
            self.market_data = pd.read_csv(MARKET_DATA_PATH)
            # Convert date column if exists
            if 'date' in self.market_data.columns:
                self.market_data['date'] = pd.to_datetime(self.market_data['date'])
            print(f"Loaded market data with {len(self.market_data)} records")
            return self.market_data
        except Exception as e:
            print(f"Error loading market data: {e}")
            return pd.DataFrame()
    
    def get_available_crops(self):
        """Get list of available crop types"""
        if self.crop_data is not None and 'crop_type' in self.crop_data.columns:
            return self.crop_data['crop_type'].unique().tolist()
        return []
    
    def get_available_regions(self):
        """Get list of available regions"""
        if self.crop_data is not None and 'region' in self.crop_data.columns:
            return self.crop_data['region'].unique().tolist()
        return []