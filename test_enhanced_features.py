#!/usr/bin/env python3
"""
Enhanced test script for AI Crop Market System
Tests all new features including weather, analytics, and notifications
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_endpoint(method, endpoint, data=None, params=None, description=""):
    """Test a single API endpoint with description"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} {method} {endpoint} - {description}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   Response: {result.get('message', 'Success')}")
                return True
            else:
                print(f"   Error: {result.get('message', 'Unknown error')}")
        else:
            print(f"   Error: {response.text}")
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {str(e)}")
        return False

def main():
    print("🌱 AI Crop Market System - Enhanced Features Test")
    print("=" * 60)
    
    # Test basic endpoints
    print("\n1. Testing Basic Endpoints:")
    test_endpoint("GET", "/", description="Home page")
    test_endpoint("GET", "/dashboard", description="Dashboard page")
    test_endpoint("GET", "/market", description="Market analysis page")
    test_endpoint("GET", "/analytics", description="Advanced analytics page")
    test_endpoint("GET", "/status", description="System status page")
    test_endpoint("GET", "/auth", description="Authentication page")
    
    # Test core API endpoints
    print("\n2. Testing Core API Endpoints:")
    test_endpoint("GET", "/api/health", description="Health check")
    test_endpoint("GET", "/api/system-status", description="System status")
    test_endpoint("GET", "/api/market-data", description="Market data")
    test_endpoint("GET", "/api/crop-data", description="Crop data")
    test_endpoint("GET", "/api/market", description="Market analysis")
    
    # Test authentication
    print("\n3. Testing Authentication:")
    test_endpoint("POST", "/api/login", {
        "username": "test@example.com",
        "password": "testpassword"
    }, description="User login")
    test_endpoint("POST", "/api/signup", {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword",
        "farmSize": "100",
        "location": "Test Location"
    }, description="User signup")
    
    # Test weather features
    print("\n4. Testing Weather Features:")
    test_endpoint("GET", "/api/weather", {"location": "Delhi"}, description="Current weather")
    test_endpoint("GET", "/api/weather/forecast", {"location": "Delhi", "days": "7"}, description="Weather forecast")
    test_endpoint("GET", "/api/weather/impact", {"location": "Delhi", "crop_type": "wheat"}, description="Weather impact on crops")
    
    # Test analytics features
    print("\n5. Testing Analytics Features:")
    test_endpoint("GET", "/api/analytics/insights", {"crop_type": "wheat", "days": "30"}, description="Market insights")
    test_endpoint("GET", "/api/analytics/performance", {"region": "all"}, description="Crop performance analysis")
    test_endpoint("GET", "/api/analytics/predictions", {"crop_type": "wheat", "days_ahead": "30"}, description="Predictive insights")
    
    # Test notification features
    print("\n6. Testing Notification Features:")
    test_endpoint("GET", "/api/notifications", {"user_id": "test_user", "limit": "10"}, description="User notifications")
    test_endpoint("GET", "/api/notifications/alerts", {"location": "Delhi", "crop_type": "wheat"}, description="Alert checking")
    test_endpoint("POST", "/api/notifications/create", {
        "user_id": "test_user",
        "alert_type": "price_threshold",
        "conditions": {"price_threshold": 200, "operator": ">"},
        "crop_type": "wheat"
    }, description="Create custom alert")
    
    # Test export features
    print("\n7. Testing Export Features:")
    test_endpoint("GET", "/api/export/data", {"type": "market", "format": "csv"}, description="Export market data as CSV")
    test_endpoint("GET", "/api/export/data", {"type": "crop", "format": "json"}, description="Export crop data as JSON")
    
    # Test crop recommendation
    print("\n8. Testing Crop Recommendation:")
    test_endpoint("POST", "/api/recommend", {
        "n": 80,
        "p": 40,
        "k": 45,
        "temperature": 29.5,
        "humidity": 70.2,
        "ph": 6.8,
        "rainfall": 210.4
    }, description="Crop recommendation")
    
    # Test market analysis
    print("\n9. Testing Market Analysis:")
    test_endpoint("POST", "/api/analyze-market", {
        "crop_type": "wheat",
        "region": "north"
    }, description="Market analysis")
    
    # Test price prediction
    print("\n10. Testing Price Prediction:")
    test_endpoint("POST", "/api/predict-prices", {
        "crop_type": "wheat",
        "days": 30
    }, description="Price prediction")
    
    print("\n" + "=" * 60)
    print("🎉 Enhanced features testing completed!")
    print("\n📊 New Features Added:")
    print("   • Weather integration with current conditions and forecasts")
    print("   • Advanced analytics dashboard with market insights")
    print("   • Notification system with price and weather alerts")
    print("   • Data export functionality (CSV/JSON)")
    print("   • Enhanced crop performance analysis")
    print("   • Predictive insights and trend analysis")
    print("   • Weather impact assessment on crops")
    print("   • Custom alert creation system")
    
    print("\n🚀 To start the enhanced system:")
    print("   python start_app.py")
    print("   Then visit: http://localhost:5000")

if __name__ == "__main__":
    main()

