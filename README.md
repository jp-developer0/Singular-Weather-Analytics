# 🌤️ Singular Weather Analytics

A simple web application that collects weather data from 10 cities worldwide, processes it, and displays beautiful charts and analytics through a clean web interface.

## ✨ What it does

- 🌍 **Fetches weather data** from 10 global cities (New York, Tokyo, London, Paris, etc.)
- 📊 **Creates charts** showing temperature comparisons, humidity, and wind analysis
- 🌐 **Web dashboard** with real-time data and interactive charts
- 💾 **Export data** as CSV files for further analysis
- 📱 **Mobile-friendly** interface that works on any device

## 🚀 Quick Start

**Requirements:** Python 3.8+ and internet connection

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   python app.py
   ```

3. **Open your browser**
   - Dashboard: http://localhost:8000
   - API docs: http://localhost:8000/docs

## 🎯 How to use

1. **Visit the dashboard** at `http://localhost:8000` to see:
   - Live weather data from 10 cities
   - Temperature, humidity, and wind statistics
   - Data tables with current conditions

2. **View charts** by clicking the visualization links:
   - Temperature comparison charts
   - Humidity and wind analysis
   - Comprehensive weather dashboard

3. **Download data** as CSV file for your own analysis

4. **API access** at `/api/data` for developers

## 🛠️ How it works

The app fetches weather data from the Open-Meteo API, processes it with pandas, and creates beautiful charts. Everything is built with FastAPI and uses clean HTML templates with proper CSS separation.

## 📁 Main Files

- **`app.py`** - Main web application (FastAPI)
- **`weather_scraper.py`** - Fetches and processes weather data
- **`visualizations.py`** - Creates charts and graphs
- **`templates/`** - HTML templates (separated from Python code)
- **`static/css/`** - CSS stylesheets (clean separation)

## 🌍 Cities Tracked

New York • Tokyo • London • Paris • Berlin • Sydney • Mumbai • Cape Town • Moscow • Rio de Janeiro

## 🧪 Testing

Run tests to make sure everything works:
```bash
python -m pytest test_app.py -v
```

---

**Simple, clean, and professional weather analytics in Python!** 🚀 