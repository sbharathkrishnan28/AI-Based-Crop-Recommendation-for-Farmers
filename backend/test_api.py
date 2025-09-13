#!/usr/bin/env python3
"""
Test script to verify all API endpoints are working correctly
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_endpoint(method, endpoint, data=None, params=None):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"✓ {method} {endpoint} - Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"  Response: {result.get('message', 'Success')}")
            else:
                print(f"  Error: {result.get('message', 'Unknown error')}")
        else:
            print(f"  Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ {method} {endpoint} - Error: {str(e)}")
        return False

def main():
    print("Testing AI Crop Market System API Endpoints")
    print("=" * 50)
    
    # Test basic endpoints
    print("\n1. Testing Basic Endpoints:")
    test_endpoint("GET", "/")
    test_endpoint("GET", "/dashboard")
    test_endpoint("GET", "/market")
    test_endpoint("GET", "/status")
    test_endpoint("GET", "/auth")
    
    # Test API endpoints
    print("\n2. Testing API Endpoints:")
    test_endpoint("GET", "/api/health")
    test_endpoint("GET", "/api/system-status")
    test_endpoint("GET", "/api/market-data")
    test_endpoint("GET", "/api/crop-data")
    test_endpoint("GET", "/api/market")
    
    # Test authentication
    print("\n3. Testing Authentication:")
    test_endpoint("POST", "/api/login", {
        "username": "test@example.com",
        "password": "testpassword"
    })
    test_endpoint("POST", "/api/signup", {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword",
        "farmSize": "100",
        "location": "Test Location"
    })
    
    # Test crop recommendation
    print("\n4. Testing Crop Recommendation:")
    test_endpoint("POST", "/api/recommend", {
        "n": 80,
        "p": 40,
        "k": 45,
        "temperature": 29.5,
        "humidity": 70.2,
        "ph": 6.8,
        "rainfall": 210.4
    })
    
    # Test market analysis
    print("\n5. Testing Market Analysis:")
    test_endpoint("POST", "/api/analyze-market", {
        "crop_type": "wheat",
        "region": "north"
    })
    
    # Test price prediction
    print("\n6. Testing Price Prediction:")
    test_endpoint("POST", "/api/predict-prices", {
        "crop_type": "wheat",
        "days": 30
    })
    
    print("\n" + "=" * 50)
    print("API testing completed!")

if __name__ == "__main__":
    main()
