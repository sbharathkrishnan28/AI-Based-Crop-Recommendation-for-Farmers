# utils/predictor.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
import os
from .data_loader import DataLoader
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MODELS_DIR

class Predictor:
    def __init__(self):
        self.data_loader = DataLoader()
        self.market_data = self.data_loader.load_market_data()
        self.models = {}
        self.models_loaded = False
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models if available"""
        try:
            if not os.path.exists(MODELS_DIR):
                os.makedirs(MODELS_DIR)
            
            # Try to load models for each crop type
            crop_types = self.market_data['crop_type'].unique() if not self.market_data.empty else []
            
            for crop in crop_types:
                model_path = os.path.join(MODELS_DIR, f'{crop}_model.pkl')
                if os.path.exists(model_path):
                    with open(model_path, 'rb') as f:
                        self.models[crop] = pickle.load(f)
            
            self.models_loaded = len(self.models) > 0
            print(f"Loaded {len(self.models)} models")
        except Exception as e:
            print(f"Error loading models: {e}")
            self.models_loaded = False
    
    def predict(self, crop_type, days=30):
        """Predict prices for a specific crop for the next days"""
        if self.market_data.empty:
            return {"error": "No market data available"}
        
        # Filter data for the specific crop
        crop_data = self.market_data[self.market_data['crop_type'] == crop_type]
        
        if crop_data.empty:
            return {"error": f"No data available for {crop_type}"}
        
        # Prepare data for prediction
        if crop_type in self.models and self.models_loaded:
            # Use pre-trained model if available
            return self._predict_with_model(crop_type, days)
        else:
            # Use simple forecasting method
            return self._simple_forecast(crop_data, days)
    
    def _predict_with_model(self, crop_type, days):
        """Predict using pre-trained model"""
        try:
            model = self.models[crop_type]
            # Create future dates for prediction
            future_dates = pd.date_range(start=pd.Timestamp.today(), periods=days, freq='D')
            # This would need proper feature preparation for your model
            predictions = [model.predict([[i]])[0] for i in range(days)]
            
            return {
                'crop_type': crop_type,
                'predictions': [
                    {'date': date.strftime('%Y-%m-%d'), 'predicted_price': price}
                    for date, price in zip(future_dates, predictions)
                ],
                'method': 'ml_model'
            }
        except Exception as e:
            print(f"Model prediction failed: {e}")
            return self._simple_forecast(
                self.market_data[self.market_data['crop_type'] == crop_type], 
                days
            )
    
    def _simple_forecast(self, crop_data, days):
        """Simple forecasting using average and trend"""
        if crop_data.empty:
            return {"error": "No data available for forecasting"}
        
        # Calculate average price and simple trend
        recent_data = crop_data.sort_values('date').tail(30)  # Last 30 days
        if recent_data.empty:
            recent_data = crop_data
        
        avg_price = recent_data['price'].mean()
        price_std = recent_data['price'].std()
        
        # Generate predictions with some randomness
        future_dates = pd.date_range(start=pd.Timestamp.today(), periods=days, freq='D')
        predictions = np.random.normal(avg_price, price_std * 0.5, days)
        
        # Ensure prices are positive
        predictions = np.maximum(predictions, avg_price * 0.5)
        
        return {
            'crop_type': crop_data['crop_type'].iloc[0] if 'crop_type' in crop_data.columns else 'unknown',
            'predictions': [
                {'date': date.strftime('%Y-%m-%d'), 'predicted_price': price}
                for date, price in zip(future_dates, predictions)
            ],
            'method': 'simple_forecast',
            'average_price': avg_price,
            'price_std': price_std
        }