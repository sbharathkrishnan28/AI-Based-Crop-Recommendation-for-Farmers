# utils/notification_service.py
from datetime import datetime, timedelta
import json

class NotificationService:
    def __init__(self):
        self.notifications = []
        self.alert_thresholds = {
            'price_change': 10,  # 10% price change
            'volatility': 0.3,   # High volatility threshold
            'trend_change': 0.5  # Significant trend change
        }
    
    def check_price_alerts(self, market_data, user_preferences=None):
        """Check for price alerts based on user preferences"""
        alerts = []
        
        if market_data is None or market_data.empty:
            return alerts
        
        for crop in market_data['crop_type'].unique():
            crop_data = market_data[market_data['crop_type'] == crop]
            if len(crop_data) < 2:
                continue
            
            current_price = crop_data.iloc[-1]['price']
            previous_price = crop_data.iloc[-2]['price']
            price_change = ((current_price - previous_price) / previous_price) * 100
            
            # Check for significant price changes
            if abs(price_change) >= self.alert_thresholds['price_change']:
                alert = {
                    'type': 'price_alert',
                    'crop': crop,
                    'message': f"{crop} price {'increased' if price_change > 0 else 'decreased'} by {abs(price_change):.1f}%",
                    'severity': 'high' if abs(price_change) > 20 else 'medium',
                    'timestamp': datetime.now().isoformat(),
                    'current_price': round(current_price, 2),
                    'price_change': round(price_change, 2)
                }
                alerts.append(alert)
        
        return alerts
    
    def check_weather_alerts(self, weather_data, crop_type):
        """Check for weather-related alerts"""
        alerts = []
        
        if not weather_data:
            return alerts
        
        temp = weather_data.get('temperature', 0)
        humidity = weather_data.get('humidity', 0)
        rainfall = weather_data.get('rainfall', 0)
        
        # Temperature alerts
        if temp > 35:
            alerts.append({
                'type': 'weather_alert',
                'crop': crop_type,
                'message': f"High temperature alert: {temp}°C - Monitor crop stress",
                'severity': 'high',
                'timestamp': datetime.now().isoformat()
            })
        elif temp < 5:
            alerts.append({
                'type': 'weather_alert',
                'crop': crop_type,
                'message': f"Low temperature alert: {temp}°C - Risk of frost damage",
                'severity': 'high',
                'timestamp': datetime.now().isoformat()
            })
        
        # Rainfall alerts
        if rainfall > 50:
            alerts.append({
                'type': 'weather_alert',
                'crop': crop_type,
                'message': f"Heavy rainfall alert: {rainfall}mm - Check for waterlogging",
                'severity': 'medium',
                'timestamp': datetime.now().isoformat()
            })
        elif rainfall < 5 and humidity < 30:
            alerts.append({
                'type': 'weather_alert',
                'crop': crop_type,
                'message': f"Drought conditions: Low rainfall and humidity - Consider irrigation",
                'severity': 'high',
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts
    
    def check_market_volatility_alerts(self, market_data):
        """Check for high market volatility"""
        alerts = []
        
        if market_data is None or market_data.empty:
            return alerts
        
        for crop in market_data['crop_type'].unique():
            crop_data = market_data[market_data['crop_type'] == crop]
            if len(crop_data) < 7:
                continue
            
            # Calculate 7-day volatility
            recent_prices = crop_data.tail(7)['price']
            returns = recent_prices.pct_change().dropna()
            volatility = returns.std() * (252 ** 0.5)  # Annualized volatility
            
            if volatility > self.alert_thresholds['volatility']:
                alerts.append({
                    'type': 'volatility_alert',
                    'crop': crop,
                    'message': f"High volatility detected for {crop}: {volatility:.1%} - Market is unstable",
                    'severity': 'medium',
                    'timestamp': datetime.now().isoformat(),
                    'volatility': round(volatility, 3)
                })
        
        return alerts
    
    def generate_daily_summary(self, market_data, weather_data, crop_type):
        """Generate daily summary notifications"""
        summary = {
            'type': 'daily_summary',
            'crop': crop_type,
            'timestamp': datetime.now().isoformat(),
            'summary': []
        }
        
        if not market_data.empty:
            crop_data = market_data[market_data['crop_type'] == crop_type]
            if not crop_data.empty:
                current_price = crop_data.iloc[-1]['price']
                avg_price = crop_data['price'].mean()
                
                if current_price > avg_price:
                    summary['summary'].append(f"Current price ({current_price:.2f}) is above average")
                else:
                    summary['summary'].append(f"Current price ({current_price:.2f}) is below average")
        
        if weather_data:
            temp = weather_data.get('temperature', 0)
            summary['summary'].append(f"Current temperature: {temp}°C")
            
            if weather_data.get('rainfall', 0) > 0:
                summary['summary'].append(f"Rainfall: {weather_data['rainfall']}mm")
        
        return summary
    
    def get_user_notifications(self, user_id, limit=10):
        """Get notifications for a specific user"""
        # In a real app, this would fetch from database
        # For demo, return recent notifications or sample data
        if not self.notifications:
            # Add some sample notifications for demo
            sample_notifications = [
                {
                    'id': 1,
                    'type': 'price_alert',
                    'message': 'Wheat prices have increased by 15% in the last week',
                    'severity': 'medium',
                    'timestamp': datetime.now().isoformat(),
                    'crop': 'wheat'
                },
                {
                    'id': 2,
                    'type': 'weather_alert',
                    'message': 'Heavy rainfall expected in your area - monitor for waterlogging',
                    'severity': 'high',
                    'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
                    'crop': 'all'
                },
                {
                    'id': 3,
                    'type': 'market_insight',
                    'message': 'Corn market showing high volatility - consider hedging strategies',
                    'severity': 'low',
                    'timestamp': (datetime.now() - timedelta(hours=6)).isoformat(),
                    'crop': 'corn'
                }
            ]
            self.notifications.extend(sample_notifications)
        
        return self.notifications[-limit:] if self.notifications else []
    
    def mark_notification_read(self, notification_id, user_id):
        """Mark a notification as read"""
        # In a real app, this would update database
        pass
    
    def create_custom_alert(self, user_id, alert_type, conditions, crop_type=None):
        """Create a custom alert for a user"""
        alert = {
            'id': len(self.notifications) + 1,
            'user_id': user_id,
            'type': 'custom_alert',
            'alert_type': alert_type,
            'conditions': conditions,
            'crop_type': crop_type,
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        self.notifications.append(alert)
        return alert
    
    def check_custom_alerts(self, market_data, weather_data):
        """Check if any custom alerts should be triggered"""
        triggered_alerts = []
        
        for notification in self.notifications:
            if not notification.get('active', False):
                continue
            
            if notification['type'] != 'custom_alert':
                continue
            
            alert_type = notification['alert_type']
            conditions = notification['conditions']
            crop_type = notification.get('crop_type')
            
            if alert_type == 'price_threshold':
                if crop_type and not market_data.empty:
                    crop_data = market_data[market_data['crop_type'] == crop_type]
                    if not crop_data.empty:
                        current_price = crop_data.iloc[-1]['price']
                        threshold = conditions.get('price_threshold', 0)
                        operator = conditions.get('operator', '>')
                        
                        if self._evaluate_condition(current_price, threshold, operator):
                            triggered_alerts.append({
                                'notification_id': notification['id'],
                                'message': f"Price alert: {crop_type} price is {current_price:.2f}",
                                'timestamp': datetime.now().isoformat()
                            })
            
            elif alert_type == 'weather_condition':
                if weather_data:
                    temp = weather_data.get('temperature', 0)
                    threshold = conditions.get('temperature_threshold', 0)
                    operator = conditions.get('operator', '>')
                    
                    if self._evaluate_condition(temp, threshold, operator):
                        triggered_alerts.append({
                            'notification_id': notification['id'],
                            'message': f"Weather alert: Temperature is {temp}°C",
                            'timestamp': datetime.now().isoformat()
                        })
        
        return triggered_alerts
    
    def _evaluate_condition(self, value, threshold, operator):
        """Evaluate a condition"""
        if operator == '>':
            return value > threshold
        elif operator == '<':
            return value < threshold
        elif operator == '>=':
            return value >= threshold
        elif operator == '<=':
            return value <= threshold
        elif operator == '==':
            return value == threshold
        return False

