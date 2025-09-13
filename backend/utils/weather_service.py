# utils/weather_service.py
import requests
import json
from datetime import datetime, timedelta
import random

class WeatherService:
    def __init__(self):
        # In a real application, you would use a weather API like OpenWeatherMap
        # For demo purposes, we'll simulate weather data
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.api_key = "demo_key"  # Replace with real API key
        
    def get_current_weather(self, location):
        """Get current weather for a location"""
        # Simulate weather data for demo
        weather_data = {
            'temperature': round(random.uniform(15, 35), 1),
            'humidity': round(random.uniform(40, 90), 1),
            'rainfall': round(random.uniform(0, 50), 1),
            'wind_speed': round(random.uniform(5, 25), 1),
            'pressure': round(random.uniform(1000, 1020), 1),
            'description': random.choice(['Clear', 'Cloudy', 'Partly Cloudy', 'Rainy', 'Sunny']),
            'location': location,
            'timestamp': datetime.now().isoformat()
        }
        return weather_data
    
    def get_weather_forecast(self, location, days=7):
        """Get weather forecast for the next few days"""
        forecast = []
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            day_weather = {
                'date': date.strftime('%Y-%m-%d'),
                'temperature': round(random.uniform(15, 35), 1),
                'humidity': round(random.uniform(40, 90), 1),
                'rainfall': round(random.uniform(0, 30), 1),
                'description': random.choice(['Clear', 'Cloudy', 'Partly Cloudy', 'Rainy', 'Sunny'])
            }
            forecast.append(day_weather)
        return forecast
    
    def get_weather_impact_on_crops(self, weather_data, crop_type):
        """Analyze weather impact on specific crops"""
        temp = weather_data['temperature']
        humidity = weather_data['humidity']
        rainfall = weather_data['rainfall']
        
        impact_analysis = {
            'crop': crop_type,
            'overall_impact': 'neutral',
            'recommendations': [],
            'risk_level': 'low'
        }
        
        # Crop-specific weather analysis
        if crop_type.lower() == 'rice':
            if rainfall > 200 and temp > 25:
                impact_analysis['overall_impact'] = 'positive'
                impact_analysis['recommendations'].append('Excellent conditions for rice cultivation')
            elif rainfall < 100:
                impact_analysis['overall_impact'] = 'negative'
                impact_analysis['recommendations'].append('Consider irrigation for rice fields')
                impact_analysis['risk_level'] = 'high'
                
        elif crop_type.lower() == 'wheat':
            if 15 <= temp <= 25 and humidity < 70:
                impact_analysis['overall_impact'] = 'positive'
                impact_analysis['recommendations'].append('Ideal conditions for wheat growth')
            elif temp > 30:
                impact_analysis['overall_impact'] = 'negative'
                impact_analysis['recommendations'].append('High temperature may stress wheat plants')
                impact_analysis['risk_level'] = 'medium'
                
        elif crop_type.lower() == 'corn':
            if 20 <= temp <= 30 and humidity > 60:
                impact_analysis['overall_impact'] = 'positive'
                impact_analysis['recommendations'].append('Good conditions for corn development')
            elif temp < 15:
                impact_analysis['overall_impact'] = 'negative'
                impact_analysis['recommendations'].append('Low temperature may slow corn growth')
                impact_analysis['risk_level'] = 'medium'
        
        return impact_analysis

