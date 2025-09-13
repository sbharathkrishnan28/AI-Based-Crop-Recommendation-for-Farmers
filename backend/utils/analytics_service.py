# utils/analytics_service.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class AnalyticsService:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.market_data = data_loader.load_market_data()
        self.crop_data = data_loader.load_crop_data()
    
    def get_market_insights(self, crop_type=None, days=30):
        """Generate comprehensive market insights"""
        if self.market_data.empty:
            return {"error": "No market data available"}
        
        # Filter data
        data = self.market_data.copy()
        if crop_type and crop_type != 'all':
            data = data[data['crop_type'] == crop_type]
        
        # Get recent data
        recent_data = data.tail(days)
        
        insights = {
            'summary': self._get_market_summary(recent_data),
            'trends': self._analyze_trends(recent_data),
            'volatility': self._calculate_volatility(recent_data),
            'seasonality': self._analyze_seasonality(data),
            'recommendations': self._generate_recommendations(recent_data)
        }
        
        return insights
    
    def _get_market_summary(self, data):
        """Get market summary statistics"""
        if data.empty:
            return {}
        
        current_price = data.iloc[-1]['price']
        previous_price = data.iloc[-2]['price'] if len(data) > 1 else current_price
        price_change = ((current_price - previous_price) / previous_price) * 100
        
        return {
            'current_price': round(current_price, 2),
            'price_change': round(price_change, 2),
            'price_change_percent': round(price_change, 2),
            'high_30d': round(data['price'].max(), 2),
            'low_30d': round(data['price'].min(), 2),
            'avg_30d': round(data['price'].mean(), 2),
            'volume_30d': len(data)
        }
    
    def _analyze_trends(self, data):
        """Analyze price trends"""
        if len(data) < 2:
            return {'trend': 'insufficient_data'}
        
        prices = data['price'].values
        x = np.arange(len(prices))
        slope = np.polyfit(x, prices, 1)[0]
        
        trend_strength = abs(slope) / np.std(prices) if np.std(prices) > 0 else 0
        
        return {
            'trend': 'upward' if slope > 0 else 'downward' if slope < 0 else 'stable',
            'trend_strength': round(trend_strength, 3),
            'slope': round(slope, 4)
        }
    
    def _calculate_volatility(self, data):
        """Calculate price volatility"""
        if len(data) < 2:
            return {'volatility': 0}
        
        returns = data['price'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252)  # Annualized volatility
        
        return {
            'volatility': round(volatility, 4),
            'risk_level': 'high' if volatility > 0.3 else 'medium' if volatility > 0.15 else 'low'
        }
    
    def _analyze_seasonality(self, data):
        """Analyze seasonal patterns"""
        if data.empty:
            return {}
        
        data['date'] = pd.to_datetime(data['date'])
        data['month'] = data['date'].dt.month
        
        monthly_avg = data.groupby('month')['price'].mean()
        
        return {
            'peak_month': int(monthly_avg.idxmax()),
            'low_month': int(monthly_avg.idxmin()),
            'seasonal_variation': round(monthly_avg.std(), 2)
        }
    
    def _generate_recommendations(self, data):
        """Generate trading recommendations"""
        if data.empty:
            return []
        
        current_price = data.iloc[-1]['price']
        avg_price = data['price'].mean()
        recent_trend = self._analyze_trends(data.tail(7))
        
        recommendations = []
        
        if current_price < avg_price * 0.9:
            recommendations.append({
                'type': 'buy',
                'message': 'Price is below average - good buying opportunity',
                'confidence': 'high'
            })
        elif current_price > avg_price * 1.1:
            recommendations.append({
                'type': 'sell',
                'message': 'Price is above average - consider selling',
                'confidence': 'medium'
            })
        
        if recent_trend['trend'] == 'upward' and recent_trend['trend_strength'] > 0.5:
            recommendations.append({
                'type': 'hold',
                'message': 'Strong upward trend - hold position',
                'confidence': 'high'
            })
        elif recent_trend['trend'] == 'downward' and recent_trend['trend_strength'] > 0.5:
            recommendations.append({
                'type': 'caution',
                'message': 'Downward trend detected - monitor closely',
                'confidence': 'medium'
            })
        
        return recommendations
    
    def get_crop_performance_analysis(self, region=None):
        """Analyze crop performance across different metrics"""
        if self.crop_data.empty:
            return {"error": "No crop data available"}
        
        data = self.crop_data.copy()
        if region and region != 'all':
            data = data[data['region'] == region]
        
        performance = {}
        
        for crop in data['crop_type'].unique():
            crop_data = data[data['crop_type'] == crop]
            
            performance[crop] = {
                'avg_production': round(crop_data['production'].mean(), 2),
                'avg_yield': round(crop_data['yield'].mean(), 2),
                'production_trend': self._calculate_trend(crop_data, 'production'),
                'yield_trend': self._calculate_trend(crop_data, 'yield'),
                'best_region': self._find_best_region(crop_data),
                'performance_score': self._calculate_performance_score(crop_data)
            }
        
        return performance
    
    def _calculate_trend(self, data, column):
        """Calculate trend for a specific column"""
        if len(data) < 2:
            return 'insufficient_data'
        
        values = data[column].values
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        return 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'
    
    def _find_best_region(self, data):
        """Find the best performing region for a crop"""
        if data.empty:
            return None
        
        region_performance = data.groupby('region')['yield'].mean()
        return region_performance.idxmax()
    
    def _calculate_performance_score(self, data):
        """Calculate overall performance score (0-100)"""
        if data.empty:
            return 0
        
        # Normalize production and yield to 0-100 scale
        production_score = min(100, (data['production'].mean() / 1000) * 100)
        yield_score = min(100, (data['yield'].mean() / 5) * 100)
        
        # Weighted average
        return round((production_score * 0.6 + yield_score * 0.4), 1)
    
    def get_predictive_insights(self, crop_type, days_ahead=30):
        """Generate predictive insights using historical patterns"""
        if self.market_data.empty:
            return {"error": "No market data available"}
        
        crop_data = self.market_data[self.market_data['crop_type'] == crop_type]
        if crop_data.empty:
            return {"error": f"No data available for {crop_type}"}
        
        # Simple trend-based prediction
        recent_data = crop_data.tail(30)
        trend = self._analyze_trends(recent_data)
        
        current_price = recent_data.iloc[-1]['price']
        predicted_price = current_price + (trend['slope'] * days_ahead)
        
        # Confidence based on trend strength and data quality
        confidence = min(95, max(30, trend['trend_strength'] * 100))
        
        return {
            'predicted_price': round(predicted_price, 2),
            'confidence': round(confidence, 1),
            'price_range': {
                'min': round(predicted_price * 0.9, 2),
                'max': round(predicted_price * 1.1, 2)
            },
            'recommendation': self._get_prediction_recommendation(trend, confidence)
        }
    
    def _get_prediction_recommendation(self, trend, confidence):
        """Get recommendation based on prediction"""
        if confidence < 50:
            return "Low confidence prediction - use with caution"
        elif trend['trend'] == 'upward':
            return "Price expected to rise - consider buying"
        elif trend['trend'] == 'downward':
            return "Price expected to fall - consider selling"
        else:
            return "Price expected to remain stable"

