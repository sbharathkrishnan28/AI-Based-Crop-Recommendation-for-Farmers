# utils/train_model.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
import os
from config import MODELS_DIR
from utils.data_loader import DataLoader

def train_models():
    """Train prediction models for each crop type"""
    data_loader = DataLoader()
    market_data = data_loader.load_market_data()
    
    if market_data.empty:
        print("No market data available for training")
        return
    
    # Create models directory if it doesn't exist
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Train a model for each crop type
    crop_types = market_data['crop_type'].unique()
    
    for crop in crop_types:
        print(f"Training model for {crop}...")
        
        # Filter data for this crop
        crop_data = market_data[market_data['crop_type'] == crop].copy()
        
        if len(crop_data) < 50:  # Need sufficient data
            print(f"Not enough data for {crop}, skipping...")
            continue
        
        # Prepare features (simplified example)
        # Convert date to numeric value (days since first date)
        crop_data['date'] = pd.to_datetime(crop_data['date'])
        crop_data['days'] = (crop_data['date'] - crop_data['date'].min()).dt.days
        
        # Simple features - in a real scenario, you'd use more sophisticated feature engineering
        X = crop_data[['days']].values
        y = crop_data['price'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model (using Random Forest as an example)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"{crop} model - MAE: {mae:.2f}, RMSE: {rmse:.2f}")
        
        # Save model
        model_path = os.path.join(MODELS_DIR, f'{crop}_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        print(f"Saved {crop} model to {model_path}")
    
    print("Model training completed")

if __name__ == '__main__':
    train_models()