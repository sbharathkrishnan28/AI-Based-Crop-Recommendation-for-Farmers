# utils/generate_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from config import CROP_DATA_PATH, MARKET_DATA_PATH

def generate_sample_data():
    """Generate sample data if no data exists"""
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(CROP_DATA_PATH), exist_ok=True)
    
    crops = ['wheat', 'corn', 'rice', 'soybean', 'barley']
    regions = ['north', 'south', 'east', 'west']
    
    # Generate crop data (overwrite existing if different structure)
    print("Generating crop data...")
    crop_data = []
    for year in range(2018, 2024):
        for crop in crops:
            for region in regions:
                production = np.random.normal(1000, 200)  # Random production value
                crop_data.append({
                    'year': year,
                    'crop_type': crop,
                    'region': region,
                    'production': max(500, production),  # Ensure positive
                    'yield': np.random.normal(3.5, 0.7)  # Yield per hectare
                })
    
    crop_df = pd.DataFrame(crop_data)
    crop_df.to_csv(CROP_DATA_PATH, index=False)
    print(f"Generated sample crop data with {len(crop_df)} records")
    
    # Generate market data (overwrite existing if different structure)
    print("Generating market data...")
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = pd.date_range(start_date, end_date)
    
    market_data = []
    base_prices = {
        'wheat': 200,
        'corn': 180,
        'rice': 300,
        'soybean': 350,
        'barley': 150
    }
    
    for date in date_range:
        for crop in crops:
            # Base price with some randomness and seasonal pattern
            base_price = base_prices[crop]
            seasonal_effect = 20 * np.sin(2 * np.pi * (date.timetuple().tm_yday / 365))
            random_effect = np.random.normal(0, 10)
            price = base_price + seasonal_effect + random_effect
            
            market_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'crop_type': crop,
                'price': max(price, base_price * 0.5),  # Ensure positive
                'demand': np.random.normal(100, 20)
            })
    
    market_df = pd.DataFrame(market_data)
    market_df.to_csv(MARKET_DATA_PATH, index=False)
    print(f"Generated sample market data with {len(market_df)} records")

if __name__ == '__main__':
    generate_sample_data()