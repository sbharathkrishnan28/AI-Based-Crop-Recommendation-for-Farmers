#!/usr/bin/env python3
"""
Startup script for AI Crop Market System
This script ensures all dependencies are met and starts the application
"""
import os
import sys
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'pandas', 'numpy', 'scikit-learn', 
        'matplotlib', 'seaborn', 'flask_cors', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages")
            return False
    
    return True

def check_data_files():
    """Check if data files exist and generate if needed"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    crop_data_path = os.path.join(data_dir, 'crop_data.csv')
    market_data_path = os.path.join(data_dir, 'market_data.csv')
    
    if not os.path.exists(crop_data_path) or not os.path.exists(market_data_path):
        print("📊 Generating sample data...")
        try:
            os.chdir('backend')
            subprocess.check_call([sys.executable, 'generate_data.py'])
            os.chdir('..')
            print("✅ Sample data generated")
        except subprocess.CalledProcessError:
            print("❌ Failed to generate sample data")
            return False
    else:
        print("✅ Data files exist")
    
    return True

def check_models():
    """Check if ML models exist and train if needed"""
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    if not os.path.exists(models_dir) or len(os.listdir(models_dir)) == 0:
        print("🤖 Training ML models...")
        try:
            os.chdir('backend')
            subprocess.check_call([sys.executable, 'train_model.py'])
            os.chdir('..')
            print("✅ ML models trained")
        except subprocess.CalledProcessError:
            print("❌ Failed to train models")
            return False
    else:
        print("✅ ML models exist")
    
    return True

def start_flask_app():
    """Start the Flask application"""
    print("\n🚀 Starting AI Crop Market System...")
    print("=" * 50)
    print("Application will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        os.chdir('backend')
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def main():
    """Main startup function"""
    print("🌱 AI Crop Market System - Startup Check")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check data files
    if not check_data_files():
        return
    
    # Check models
    if not check_models():
        return
    
    print("\n✅ All checks passed! Starting application...")
    time.sleep(2)
    
    # Start the application
    start_flask_app()

if __name__ == "__main__":
    main()
