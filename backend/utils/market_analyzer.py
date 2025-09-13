# utils/market_analyzer.py
import pandas as pd
import numpy as np
from .data_loader import DataLoader

class MarketAnalyzer:
    def __init__(self):
        self.data_loader = DataLoader()
        self.crop_data = self.data_loader.load_crop_data()
        self.market_data = self.data_loader.load_market_data()
    
    def analyze(self, crop_type=None, region=None):
        """Analyze market trends for specific crop and region"""
        # Filter data based on parameters
        crop_filtered = self.crop_data.copy()
        market_filtered = self.market_data.copy()
        
        if crop_type and crop_type != 'all':
            crop_filtered = crop_filtered[crop_filtered['crop_type'] == crop_type]
            market_filtered = market_filtered[market_filtered['crop_type'] == crop_type]
        
        if region and region != 'all':
            crop_filtered = crop_filtered[crop_filtered['region'] == region]
            # Assuming market data has region column
            if 'region' in market_filtered.columns:
                market_filtered = market_filtered[market_filtered['region'] == region]
        
        # Perform analysis
        analysis = {
            'crop_type': crop_type if crop_type else 'all',
            'region': region if region else 'all',
            'total_production': crop_filtered['production'].sum() if 'production' in crop_filtered.columns else 0,
            'average_price': market_filtered['price'].mean() if 'price' in market_filtered.columns else 0,
            'price_trend': self._calculate_trend(market_filtered, 'price'),
            'production_trend': self._calculate_trend(crop_filtered, 'production'),
            'records_analyzed': len(market_filtered)
        }
        
        return analysis
    
    def _calculate_trend(self, data, column):
        """Calculate trend for a specific column"""
        if data.empty or column not in data.columns:
            return 'insufficient data'
        
        # Simple trend calculation
        if 'date' in data.columns:
            sorted_data = data.sort_values('date')
            values = sorted_data[column].values
            
            if len(values) > 1:
                # Simple linear trend
                trend = (values[-1] - values[0]) / values[0] * 100
                return f"{trend:.2f}%"
        
        return 'stable'