# utils/app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import pandas as pd
import json
import os
from datetime import datetime

# Import your custom modules
from utils.market_analyzer import MarketAnalyzer
from utils.predictor import Predictor
from utils.data_loader import DataLoader
from utils.weather_service import WeatherService
from utils.analytics_service import AnalyticsService
from utils.notification_service import NotificationService

app = Flask(__name__, 
            template_folder=os.path.join(os.pardir, 'frontend'),
            static_folder=os.path.join(os.pardir, 'frontend', 'static'))
app.secret_key = 'ai-crop-market-secret-key-2023'
CORS(app)

# Initialize components
data_loader = DataLoader()
market_analyzer = MarketAnalyzer()
predictor = Predictor()
weather_service = WeatherService()
analytics_service = AnalyticsService(data_loader)
notification_service = NotificationService()

# Load data
try:
    crop_data = data_loader.load_crop_data()
    market_data = data_loader.load_market_data()
    print("Data loaded successfully")
except Exception as e:
    print(f"Error loading data: {e}")
    crop_data = pd.DataFrame()
    market_data = pd.DataFrame()

# Routes for serving frontend pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/market')
def market():
    return render_template('market.html')

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

# API Routes for backend functionality
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Simple authentication (replace with proper authentication in production)
    # Accept any email/password combination for demo purposes
    if username and password:
        session['user'] = {
            'email': username,
            'name': username.split('@')[0] if '@' in username else username
        }
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    farm_size = data.get('farmSize')
    location = data.get('location')
    
    # Simple validation (replace with proper validation in production)
    if not all([name, email, password, farm_size, location]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    # In a real app, you would hash the password and store in database
    # For now, just store in session
    session['user'] = {
        'name': name,
        'email': email,
        'farm_size': farm_size,
        'location': location
    }
    
    return jsonify({'success': True, 'message': 'Account created successfully'})

@app.route('/api/logout')
def logout():
    session.pop('user', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/market-data')
def get_market_data():
    try:
        # Get date range from request parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        crop_type = request.args.get('crop_type', 'all')
        
        # Filter data based on parameters
        filtered_data = market_data.copy()
        
        if start_date:
            filtered_data = filtered_data[filtered_data['date'] >= start_date]
        if end_date:
            filtered_data = filtered_data[filtered_data['date'] <= end_date]
        if crop_type != 'all':
            filtered_data = filtered_data[filtered_data['crop_type'] == crop_type]
        
        # Convert to JSON format for frontend
        result = filtered_data.to_dict(orient='records')
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/market')
def get_market():
    try:
        crop_name = request.args.get('crop', 'all')
        
        # Filter market data by crop
        if crop_name != 'all':
            filtered_data = market_data[market_data['crop_type'] == crop_name].copy()
        else:
            filtered_data = market_data.copy()
        
        # Get latest prices and trends
        latest_prices = {}
        price_trends = {}
        
        for crop in filtered_data['crop_type'].unique():
            crop_data = filtered_data[filtered_data['crop_type'] == crop]
            if not crop_data.empty:
                latest_price = crop_data.iloc[-1]['price']
                price_change = 0
                if len(crop_data) > 1:
                    price_change = ((latest_price - crop_data.iloc[-2]['price']) / crop_data.iloc[-2]['price']) * 100
                
                latest_prices[crop] = {
                    'price': round(latest_price, 2),
                    'change': round(price_change, 2),
                    'trend': 'up' if price_change > 0 else 'down' if price_change < 0 else 'stable'
                }
                
                # Calculate 7-day trend
                recent_data = crop_data.tail(7)
                if len(recent_data) > 1:
                    trend_slope = (recent_data.iloc[-1]['price'] - recent_data.iloc[0]['price']) / len(recent_data)
                    price_trends[crop] = round(trend_slope, 2)
        
        return jsonify({
            'success': True, 
            'latest_prices': latest_prices,
            'price_trends': price_trends,
            'data': filtered_data.tail(30).to_dict(orient='records')  # Last 30 records
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/crop-data')
def get_crop_data():
    try:
        # Get filters from request parameters
        region = request.args.get('region', 'all')
        crop_type = request.args.get('crop_type', 'all')
        
        # Filter data based on parameters
        filtered_data = crop_data.copy()
        
        if region != 'all':
            filtered_data = filtered_data[filtered_data['region'] == region]
        if crop_type != 'all':
            filtered_data = filtered_data[filtered_data['crop_type'] == crop_type]
        
        # Convert to JSON format for frontend
        result = filtered_data.to_dict(orient='records')
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/analyze-market', methods=['POST'])
def analyze_market():
    try:
        data = request.get_json()
        crop_type = data.get('crop_type')
        region = data.get('region')
        
        # Perform market analysis
        analysis_result = market_analyzer.analyze(crop_type, region)
        
        return jsonify({'success': True, 'analysis': analysis_result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/predict-prices', methods=['POST'])
def predict_prices():
    try:
        data = request.get_json()
        crop_type = data.get('crop_type')
        days = data.get('days', 30)  # Default to 30 days prediction
        
        # Get price predictions
        predictions = predictor.predict(crop_type, days)
        
        return jsonify({'success': True, 'predictions': predictions})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend_crop():
    try:
        data = request.get_json()
        n = data.get('n')
        p = data.get('p')
        k = data.get('k')
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        ph = data.get('ph')
        rainfall = data.get('rainfall')
        
        # Simple crop recommendation logic (replace with ML model)
        recommendations = []
        
        # Basic rules for crop recommendation
        if temperature > 25 and rainfall > 200:
            recommendations.append({'crop': 'Rice', 'confidence': 0.85, 'reason': 'High temperature and rainfall suitable for rice'})
        if temperature > 20 and ph > 6.5:
            recommendations.append({'crop': 'Wheat', 'confidence': 0.80, 'reason': 'Moderate temperature and neutral pH suitable for wheat'})
        if temperature > 22 and humidity > 70:
            recommendations.append({'crop': 'Corn', 'confidence': 0.75, 'reason': 'Warm temperature and high humidity suitable for corn'})
        if ph > 6.0 and rainfall > 150:
            recommendations.append({'crop': 'Soybean', 'confidence': 0.70, 'reason': 'Neutral pH and adequate rainfall suitable for soybean'})
        
        # If no specific recommendations, suggest based on general conditions
        if not recommendations:
            recommendations.append({'crop': 'Barley', 'confidence': 0.60, 'reason': 'General conditions suitable for barley'})
        
        return jsonify({'success': True, 'recommendations': recommendations})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/health')
def health_check():
    try:
        return jsonify({
            'success': True, 
            'status': 'healthy',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/weather')
def get_weather():
    try:
        location = request.args.get('location', 'Delhi')
        weather_data = weather_service.get_current_weather(location)
        return jsonify({'success': True, 'weather': weather_data})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/weather/forecast')
def get_weather_forecast():
    try:
        location = request.args.get('location', 'Delhi')
        days = int(request.args.get('days', 7))
        forecast = weather_service.get_weather_forecast(location, days)
        return jsonify({'success': True, 'forecast': forecast})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/weather/impact')
def get_weather_impact():
    try:
        location = request.args.get('location', 'Delhi')
        crop_type = request.args.get('crop_type', 'wheat')
        
        weather_data = weather_service.get_current_weather(location)
        impact = weather_service.get_weather_impact_on_crops(weather_data, crop_type)
        
        return jsonify({'success': True, 'weather': weather_data, 'impact': impact})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/analytics/insights')
def get_analytics_insights():
    try:
        crop_type = request.args.get('crop_type', 'all')
        days = int(request.args.get('days', 30))
        
        insights = analytics_service.get_market_insights(crop_type, days)
        return jsonify({'success': True, 'insights': insights})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/analytics/performance')
def get_crop_performance():
    try:
        region = request.args.get('region', 'all')
        performance = analytics_service.get_crop_performance_analysis(region)
        return jsonify({'success': True, 'performance': performance})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/analytics/predictions')
def get_predictive_insights():
    try:
        crop_type = request.args.get('crop_type', 'wheat')
        days_ahead = int(request.args.get('days_ahead', 30))
        
        insights = analytics_service.get_predictive_insights(crop_type, days_ahead)
        return jsonify({'success': True, 'predictions': insights})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/notifications')
def get_notifications():
    try:
        user_id = request.args.get('user_id', 'default')
        limit = int(request.args.get('limit', 10))
        
        notifications = notification_service.get_user_notifications(user_id, limit)
        return jsonify({'success': True, 'notifications': notifications})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/notifications/alerts')
def check_alerts():
    try:
        location = request.args.get('location', 'Delhi')
        crop_type = request.args.get('crop_type', 'wheat')
        
        # Get weather data
        weather_data = weather_service.get_current_weather(location)
        
        # Check various alerts
        price_alerts = notification_service.check_price_alerts(market_data)
        weather_alerts = notification_service.check_weather_alerts(weather_data, crop_type)
        volatility_alerts = notification_service.check_market_volatility_alerts(market_data)
        
        all_alerts = price_alerts + weather_alerts + volatility_alerts
        
        return jsonify({'success': True, 'alerts': all_alerts})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/notifications/create', methods=['POST'])
def create_alert():
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default')
        alert_type = data.get('alert_type')
        conditions = data.get('conditions', {})
        crop_type = data.get('crop_type')
        
        alert = notification_service.create_custom_alert(user_id, alert_type, conditions, crop_type)
        return jsonify({'success': True, 'alert': alert})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/export/data')
def export_data():
    try:
        data_type = request.args.get('type', 'market')
        format_type = request.args.get('format', 'csv')
        
        if data_type == 'market':
            data = market_data
        elif data_type == 'crop':
            data = crop_data
        else:
            return jsonify({'success': False, 'message': 'Invalid data type'}), 400
        
        if format_type == 'csv':
            csv_data = data.to_csv(index=False)
            return jsonify({'success': True, 'data': csv_data, 'type': 'csv'})
        elif format_type == 'json':
            json_data = data.to_dict(orient='records')
            return jsonify({'success': True, 'data': json_data, 'type': 'json'})
        else:
            return jsonify({'success': False, 'message': 'Invalid format type'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/system-status')
def system_status():
    try:
        # Check if models are loaded and data is available
        models_loaded = predictor.models_loaded if hasattr(predictor, 'models_loaded') else False
        data_available = not crop_data.empty and not market_data.empty
        
        status = {
            'data_available': data_available,
            'models_loaded': models_loaded,
            'crop_records': len(crop_data),
            'market_records': len(market_data),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'services': {
                'weather': True,
                'analytics': True,
                'notifications': True
            }
        }
        
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)