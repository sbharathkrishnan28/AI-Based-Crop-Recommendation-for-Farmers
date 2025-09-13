# AI Crop Market System (Krishisalah)

A comprehensive AI-powered crop recommendation and market analysis system that helps farmers make informed decisions about crop selection and market timing.

## 🌟 Features

### Core Features
- **Crop Recommendation**: AI-powered crop suggestions based on soil properties and environmental conditions
- **Market Analysis**: Real-time market trends and price predictions
- **Price Forecasting**: ML-based price predictions for different crops
- **User Dashboard**: Personalized dashboard with insights and recommendations
- **System Status**: Real-time monitoring of system health and data availability

### Enhanced Features
- **Weather Integration**: Current weather conditions and 7-day forecasts
- **Advanced Analytics**: Comprehensive market insights and trend analysis
- **Smart Notifications**: Price alerts, weather warnings, and custom notifications
- **Data Export**: Export market and crop data in CSV/JSON formats
- **Performance Analysis**: Crop performance metrics across different regions
- **Predictive Insights**: Advanced forecasting with confidence levels
- **Weather Impact Assessment**: Analysis of weather effects on crop growth
- **Custom Alerts**: User-defined price and weather threshold alerts
- **Mobile Responsive**: Optimized for mobile and tablet devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation & Setup

1. **Clone or download the project**
   ```bash
   # If you have git
   git clone <repository-url>
   cd ai-crop-market-system
   
   # Or simply extract the downloaded files
   ```

2. **Run the startup script**
   ```bash
   python start_app.py
   ```
   
   This script will:
   - Check Python version compatibility
   - Install required dependencies
   - Generate sample data
   - Train ML models
   - Start the Flask application

3. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - The application will start with the authentication page

### Manual Setup (Alternative)

If you prefer to set up manually:

1. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Generate sample data**
   ```bash
   cd backend
   python generate_data.py
   ```

3. **Train ML models**
   ```bash
   python train_model.py
   ```

4. **Start the application**
   ```bash
   python app.py
   ```

## 📱 How to Use

### 1. Authentication
- Visit `http://localhost:5000`
- Click "Get Started" to create an account or login
- Fill in your details (any email/password works for demo)

### 2. Dashboard
- After login, you'll see your personalized dashboard
- View system status and quick insights
- Access crop recommendation tool

### 3. Crop Recommendation
- Enter soil properties (N, P, K levels)
- Enter environmental conditions (temperature, humidity, pH, rainfall)
- Click "Get Recommendation" to receive AI-powered crop suggestions

### 4. Market Analysis
- Navigate to "Market Analysis" from the dashboard
- View real-time price trends for different crops
- Analyze market data and price predictions

### 5. System Status
- Check system health and data availability
- Monitor ML model status
- View data statistics

## 🏗️ Project Structure

```
ai-crop-market-system/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── generate_data.py       # Sample data generator
│   ├── train_model.py         # ML model training
│   ├── requirements.txt       # Python dependencies
│   └── utils/
│       ├── data_loader.py     # Data loading utilities
│       ├── market_analyzer.py # Market analysis logic
│       └── predictor.py       # Price prediction models
├── frontend/
│   ├── index.html            # Landing page
│   ├── auth.html             # Login/Signup page
│   ├── dashboard.html        # Main dashboard
│   ├── market.html           # Market analysis page
│   ├── status.html           # System status page
│   └── components/
│       └── navbar.html       # Navigation component
├── data/
│   ├── crop_data.csv         # Crop production data
│   └── market_data.csv       # Market price data
├── models/
│   ├── wheat_model.pkl       # Trained wheat price model
│   ├── corn_model.pkl        # Trained corn price model
│   ├── rice_model.pkl        # Trained rice price model
│   ├── soybean_model.pkl     # Trained soybean price model
│   └── barley_model.pkl      # Trained barley price model
├── start_app.py              # Startup script
└── README.md                 # This file
```

## 🔧 API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/signup` - User registration
- `GET /api/logout` - User logout

### Data & Analysis
- `GET /api/market-data` - Get market data
- `GET /api/crop-data` - Get crop data
- `GET /api/market` - Get market analysis
- `POST /api/recommend` - Get crop recommendations
- `POST /api/analyze-market` - Analyze market trends
- `POST /api/predict-prices` - Predict crop prices

### Weather Integration
- `GET /api/weather` - Get current weather
- `GET /api/weather/forecast` - Get weather forecast
- `GET /api/weather/impact` - Get weather impact on crops

### Advanced Analytics
- `GET /api/analytics/insights` - Get market insights
- `GET /api/analytics/performance` - Get crop performance analysis
- `GET /api/analytics/predictions` - Get predictive insights

### Notifications & Alerts
- `GET /api/notifications` - Get user notifications
- `GET /api/notifications/alerts` - Check for alerts
- `POST /api/notifications/create` - Create custom alert

### Data Export
- `GET /api/export/data` - Export data (CSV/JSON)

### System
- `GET /api/health` - Health check
- `GET /api/system-status` - System status

## 🤖 Machine Learning Models

The system uses Random Forest regression models for price prediction:

- **Training Data**: Historical market prices with seasonal patterns
- **Features**: Time-based features (days since start date)
- **Models**: Separate models for each crop type (wheat, corn, rice, soybean, barley)
- **Performance**: Models are evaluated using MAE and RMSE metrics

## 📊 Sample Data

The system comes with generated sample data:

- **Crop Data**: 120 records with production data across 5 crops and 4 regions
- **Market Data**: 7,305 records with daily price data over 4 years
- **Crops**: Wheat, Corn, Rice, Soybean, Barley
- **Regions**: North, South, East, West

## 🛠️ Customization

### Adding New Crops
1. Update crop lists in `generate_data.py`
2. Retrain models with `train_model.py`
3. Update frontend crop selection options

### Modifying ML Models
1. Edit `utils/predictor.py` to change model architecture
2. Update feature engineering in `train_model.py`
3. Retrain models with new configuration

### Styling Changes
1. Modify CSS in individual HTML files
2. Update component styles in `components/navbar.html`
3. Customize color scheme and layout

## 🐛 Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   - Change port in `backend/app.py` (line 236)
   - Update frontend API calls to use new port

2. **Module not found errors**
   - Ensure you're running from the correct directory
   - Check Python path and virtual environment

3. **Data not loading**
   - Run `python backend/generate_data.py`
   - Check file permissions in data directory

4. **Models not found**
   - Run `python backend/train_model.py`
   - Ensure models directory exists

### Getting Help

- Check the console output for error messages
- Verify all dependencies are installed
- Ensure data files are generated correctly
- Check that models are trained and saved

## 🔮 Future Enhancements

- Real-time weather data integration
- Advanced ML models (LSTM, XGBoost)
- User authentication with database
- Mobile app development
- Real market data integration
- Multi-language support

## 📄 License

This project is for educational and demonstration purposes.

## 👥 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

---

**Happy Farming! 🌱**
