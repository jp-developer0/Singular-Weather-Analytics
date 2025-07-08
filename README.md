# 🌤️ Singular Weather Analytics Platform

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.105.0-green.svg)
![Pandas](https://img.shields.io/badge/pandas-2.1.4-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A professional weather data scraping, processing, and visualization platform built for **Singular** - the leading marketing analytics and attribution platform. This application demonstrates advanced data engineering, analytics, and web development capabilities.

## 🎯 Project Overview

This application showcases:
- **Data Collection**: Professional weather data scraping from Open-Meteo API
- **Data Processing**: Advanced pandas operations with temperature/wind conversions
- **Business Intelligence**: Analytics insights and key performance indicators
- **Data Visualization**: Professional charts using matplotlib and seaborn
- **Web API**: Modern FastAPI application with comprehensive endpoints
- **Production Ready**: Proper error handling, logging, and configuration management

## 🏗️ Architecture

```
Singular Weather Analytics Platform
├── 🌐 Web Layer (FastAPI)
│   ├── Interactive Dashboard
│   ├── REST API Endpoints  
│   └── File Download Services
├── 📊 Analytics Layer
│   ├── Data Processing (Pandas)
│   ├── Statistical Analysis
│   └── Business Intelligence
├── 📈 Visualization Layer
│   ├── Temperature Analysis
│   ├── Humidity & Wind Charts
│   └── Comprehensive Dashboards
└── 🔌 Data Layer
    ├── Open-Meteo API Integration
    ├── CSV Export Functionality
    └── Real-time Data Caching
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection for API access

### Installation

1. **Clone and Setup**
   ```bash
   cd singular
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment** (Optional)
   ```bash
   cp .env.example .env
   # Edit .env file if needed
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Platform**
   - 🌐 Dashboard: http://localhost:8000
   - 📚 API Documentation: http://localhost:8000/docs
   - 🔍 API Explorer: http://localhost:8000/redoc

## 📱 Application Features

### 🏠 Interactive Dashboard
- **Real-time Weather Data**: Live data from 10 global cities
- **Key Performance Indicators**: Temperature, humidity, and wind analytics
- **Responsive Design**: Mobile-friendly, professional interface
- **Data Tables**: Sortable, formatted weather information

### 📊 Data Visualizations
- **Temperature Comparison**: Celsius and Fahrenheit bar charts
- **Humidity & Wind Analysis**: Multi-dimensional analysis charts
- **Comprehensive Dashboard**: Executive-level analytics overview
- **High-Resolution Output**: 300 DPI professional charts

### 🔗 API Endpoints

#### Core Data Endpoints
- `GET /` - Interactive dashboard homepage
- `GET /api/data` - Complete weather data in JSON format
- `GET /api/insights` - Business intelligence insights
- `GET /api/cities` - List of monitored cities

#### Visualization Endpoints
- `GET /charts/temperature_comparison` - Temperature analysis chart
- `GET /charts/humidity_wind_analysis` - Humidity and wind charts
- `GET /charts/comprehensive_dashboard` - Executive dashboard

#### Utility Endpoints
- `GET /download/csv` - Download data as CSV file
- `POST /update` - Trigger manual data refresh
- `GET /health` - System health check

## 🛠️ Technical Implementation

### Data Collection
```python
# Professional API integration with error handling
weather_scraper = WeatherScraper()
weather_df = weather_scraper.scrape_all_cities()
```

### Data Processing
```python
# Temperature conversion (C to F)
df['temperature_f'] = df['temperature_c'] * 9/5 + 32

# Wind speed conversion (m/s to mph)  
df['wind_speed_mph'] = df['wind_speed_ms'] * 2.237
```

### Business Intelligence
```python
# Generate analytics insights
insights = weather_scraper.get_weather_insights(weather_df)
# Includes: hottest/coldest cities, averages, extremes
```

### Professional Visualizations
```python
# High-quality charts with business styling
visualizer = WeatherVisualizer()
charts = visualizer.generate_all_visualizations(df, insights)
```

## 📁 Project Structure

```
singular/
├── 📄 app.py                    # FastAPI web application
├── 🌡️ weather_scraper.py       # Data collection and processing
├── 📊 visualizations.py        # Chart generation and analytics
├── ⚙️ config.py                # Configuration management
├── 📋 requirements.txt         # Python dependencies
├── 📖 README.md               # This documentation
├── 📁 static/                 # Static web assets
│   └── 📁 charts/            # Generated visualization files
├── 📄 weather_data.csv        # Exported data file
└── 🧪 test_app.py            # Application tests
```

## 🎨 Sample Data Output

| City | Temperature (°C) | Temperature (°F) | Humidity (%) | Wind Speed (m/s) | Wind Speed (mph) |
|------|------------------|------------------|--------------|------------------|------------------|
| Mumbai | 28.5 | 83.3 | 78 | 3.2 | 7.2 |
| Sydney | 22.1 | 71.8 | 65 | 4.8 | 10.7 |
| New York | 15.3 | 59.5 | 72 | 5.1 | 11.4 |
| London | 12.7 | 54.9 | 84 | 6.2 | 13.9 |
| Tokyo | 18.9 | 66.0 | 69 | 2.8 | 6.3 |

## 🧪 Testing

### Run Data Collection Test
```bash
python weather_scraper.py
```

### Run Visualization Test  
```bash
python visualizations.py
```

### Run Full Application Test
```bash
python test_app.py
```

### API Testing
```bash
# Test API endpoints
curl http://localhost:8000/api/data
curl http://localhost:8000/api/insights
curl http://localhost:8000/health
```

## 🔧 Configuration Options

### Environment Variables (.env)
```env
# API Configuration
OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1/current

# Server Configuration  
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Data Configuration
OUTPUT_CSV_FILE=weather_data.csv
CHARTS_DIR=static/charts
```

### Monitored Cities
The application tracks weather for these global cities:
- 🗽 New York, USA
- 🗼 Tokyo, Japan  
- 🏰 London, UK
- 🗼 Paris, France
- 🏛️ Berlin, Germany
- 🏖️ Sydney, Australia
- 🏙️ Mumbai, India
- ⛰️ Cape Town, South Africa
- 🏛️ Moscow, Russia
- 🏖️ Rio de Janeiro, Brazil

## 📈 Business Intelligence Features

### Key Performance Indicators (KPIs)
- **Temperature Analytics**: Average, min/max, hottest/coldest cities
- **Humidity Insights**: Most/least humid locations, distributions
- **Wind Analysis**: Speed comparisons, weather patterns
- **Data Quality Metrics**: Collection success rates, update timestamps

### Analytics Capabilities
- **Comparative Analysis**: City-by-city weather comparisons
- **Trend Visualization**: Distribution charts and scatter plots
- **Executive Dashboards**: High-level overview with key insights
- **Export Functionality**: CSV downloads with timestamp

## 🔒 Production Considerations

### Security Features
- **Rate Limiting**: Respectful API usage with delays
- **Error Handling**: Comprehensive exception management
- **Input Validation**: Safe parameter handling
- **Health Monitoring**: System status endpoints

### Performance Optimizations
- **Data Caching**: In-memory storage for quick access
- **Background Tasks**: Async data updates
- **Efficient Processing**: Pandas vectorized operations
- **High-Quality Output**: 300 DPI visualization export

## 🌟 Singular Integration Benefits

This application demonstrates capabilities perfectly aligned with **Singular's** marketing analytics platform:

- **Data Engineering Excellence**: Professional ETL pipelines
- **Analytics Expertise**: Statistical analysis and insights generation
- **Visualization Mastery**: Business-ready charts and dashboards  
- **API Development**: Modern, scalable web services
- **Production Quality**: Error handling, logging, monitoring

## 🤝 Contributing

This project showcases professional development practices:
- Clean, modular code architecture
- Comprehensive documentation
- Type hints and error handling
- Professional logging and monitoring
- Modern Python packaging

## 📄 License

This project is created as a technical demonstration for **Singular** and showcases production-ready development practices.

---

**Built with ❤️ for Singular Analytics Platform**

*Demonstrating professional data engineering, analytics, and web development capabilities* 