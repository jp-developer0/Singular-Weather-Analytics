"""
Singular Weather Analytics Web Application
Professional FastAPI application for weather data analytics and visualization
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import pandas as pd
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
import asyncio
import uvicorn

# Import our custom modules
from weather_scraper import WeatherScraper
from visualizations import WeatherVisualizer
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Singular Weather Analytics API",
    description="Professional weather data collection, processing, and visualization platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Global variables to cache data
cached_weather_data: Optional[pd.DataFrame] = None
cached_insights: Optional[Dict] = None
cached_charts: Optional[Dict[str, str]] = None
last_update_time: Optional[datetime] = None

# Initialize our services
weather_scraper = WeatherScraper()
weather_visualizer = WeatherVisualizer()

async def update_weather_data():
    """
    Background task to update weather data
    """
    global cached_weather_data, cached_insights, cached_charts, last_update_time
    
    try:
        logger.info("Starting weather data update")
        
        # Fetch fresh weather data
        weather_df = weather_scraper.scrape_all_cities()
        
        if weather_df.empty:
            logger.error("No weather data received")
            return
        
        # Generate insights
        insights = weather_scraper.get_weather_insights(weather_df)
        
        # Generate visualizations
        chart_paths = weather_visualizer.generate_all_visualizations(weather_df, insights)
        
        # Export to CSV
        csv_path = config.OUTPUT_CSV_FILE
        weather_df.to_csv(csv_path, index=False)
        
        # Update cache
        cached_weather_data = weather_df
        cached_insights = insights
        cached_charts = chart_paths
        last_update_time = datetime.now()
        
        logger.info(f"Weather data updated successfully for {len(weather_df)} cities")
        
    except Exception as e:
        logger.error(f"Error updating weather data: {e}")

@app.on_event("startup")
async def startup_event():
    """
    Initialize the application with fresh weather data
    """
    logger.info("🚀 Starting Singular Weather Analytics Application")
    
    # Ensure required directories exist
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    
    # Load initial weather data
    await update_weather_data()

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """
    Homepage with weather analytics dashboard
    """
    if cached_weather_data is None:
        return HTMLResponse("""
        <html>
        <head>
            <title>Singular Weather Analytics</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .error { color: #e74c3c; }
            </style>
        </head>
        <body>
            <h1>🌤️ Singular Weather Analytics</h1>
            <p class="error">Weather data is currently being loaded. Please refresh in a moment.</p>
            <a href="/update">Refresh Data</a>
        </body>
        </html>
        """)
    
    # Generate HTML dashboard
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Singular Weather Analytics Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }}
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .stat-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .stat-value {{
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }}
            .data-table {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                overflow-x: auto;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f8f9fa;
                font-weight: bold;
            }}
            .actions {{
                text-align: center;
                margin: 30px 0;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 24px;
                margin: 0 10px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                transition: background 0.3s;
            }}
            .btn:hover {{
                background: #5a6fd8;
            }}
            .btn.secondary {{
                background: #6c757d;
            }}
            .btn.secondary:hover {{
                background: #5a6268;
            }}
            .charts-section {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .chart-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }}
            .chart-link {{
                display: block;
                text-align: center;
                padding: 20px;
                border: 2px dashed #ddd;
                border-radius: 10px;
                text-decoration: none;
                color: #667eea;
                font-weight: bold;
                transition: all 0.3s;
            }}
            .chart-link:hover {{
                border-color: #667eea;
                background: #f8f9fa;
            }}
            .footer {{
                text-align: center;
                color: white;
                margin-top: 40px;
                padding: 20px;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌤️ Singular Weather Analytics</h1>
                <p>Global Weather Intelligence Dashboard</p>
                <p>Last Updated: {last_update_time.strftime('%Y-%m-%d %H:%M:%S') if last_update_time else 'Unknown'}</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{cached_insights['total_cities']}</div>
                    <div>Cities Analyzed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{cached_insights['temperature_stats']['avg_temperature_c']}°C</div>
                    <div>Average Temperature</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{cached_insights['humidity_stats']['avg_humidity']}%</div>
                    <div>Average Humidity</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{cached_insights['wind_stats']['avg_wind_speed_mph']} mph</div>
                    <div>Average Wind Speed</div>
                </div>
            </div>
            
            <div class="data-table">
                <h2>📊 Weather Data Summary</h2>
                <table>
                    <thead>
                        <tr>
                            <th>City</th>
                            <th>Temperature (°C)</th>
                            <th>Temperature (°F)</th>
                            <th>Humidity (%)</th>
                            <th>Wind Speed (m/s)</th>
                            <th>Wind Speed (mph)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {_generate_table_rows(cached_weather_data)}
                    </tbody>
                </table>
            </div>
            
            <div class="charts-section">
                <h2>📈 Data Visualizations</h2>
                <div class="chart-grid">
                    <a href="/charts/temperature_comparison" class="chart-link">
                        📊 Temperature Comparison
                    </a>
                    <a href="/charts/humidity_wind_analysis" class="chart-link">
                        💨 Humidity & Wind Analysis
                    </a>
                    <a href="/charts/comprehensive_dashboard" class="chart-link">
                        🎯 Comprehensive Dashboard
                    </a>
                </div>
            </div>
            
            <div class="actions">
                <a href="/api/data" class="btn">📋 View JSON Data</a>
                <a href="/download/csv" class="btn">💾 Download CSV</a>
                <a href="/update" class="btn secondary">🔄 Refresh Data</a>
                <a href="/docs" class="btn secondary">📚 API Documentation</a>
            </div>
            
            <div class="footer">
                <p>🚀 Powered by Singular Analytics Platform | Built with FastAPI, Pandas & Python</p>
                <p>Professional weather data collection and business intelligence</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(html_content)

def _generate_table_rows(df: pd.DataFrame) -> str:
    """Generate HTML table rows from DataFrame"""
    if df is None or df.empty:
        return "<tr><td colspan='6'>No data available</td></tr>"
    
    rows = []
    for _, row in df.iterrows():
        rows.append(f"""
        <tr>
            <td><strong>{row['city']}</strong></td>
            <td>{row['temperature_c']:.1f}°C</td>
            <td>{row['temperature_f']:.1f}°F</td>
            <td>{row['humidity']:.0f}%</td>
            <td>{row['wind_speed_ms']:.1f} m/s</td>
            <td>{row['wind_speed_mph']:.1f} mph</td>
        </tr>
        """)
    
    return "".join(rows)

@app.get("/api/data")
async def get_weather_data():
    """
    API endpoint to get current weather data as JSON
    """
    if cached_weather_data is None:
        raise HTTPException(status_code=503, detail="Weather data not available")
    
    return {
        "data": cached_weather_data.to_dict('records'),
        "insights": cached_insights,
        "last_updated": last_update_time.isoformat() if last_update_time else None,
        "total_cities": len(cached_weather_data)
    }

@app.get("/api/insights")
async def get_weather_insights():
    """
    API endpoint to get weather insights and analytics
    """
    if cached_insights is None:
        raise HTTPException(status_code=503, detail="Weather insights not available")
    
    return cached_insights

@app.get("/charts/{chart_name}")
async def get_chart(chart_name: str):
    """
    Serve weather visualization charts
    """
    if cached_charts is None or chart_name not in cached_charts:
        raise HTTPException(status_code=404, detail="Chart not found")
    
    chart_path = cached_charts[chart_name]
    
    if not os.path.exists(chart_path):
        raise HTTPException(status_code=404, detail="Chart file not found")
    
    return FileResponse(chart_path, media_type="image/png")

@app.get("/download/csv")
async def download_csv():
    """
    Download weather data as CSV file
    """
    csv_path = config.OUTPUT_CSV_FILE
    
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    
    return FileResponse(
        csv_path, 
        media_type="text/csv", 
        filename=f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

@app.post("/update")
async def update_data(background_tasks: BackgroundTasks):
    """
    Trigger a manual update of weather data
    """
    background_tasks.add_task(update_weather_data)
    
    return JSONResponse({
        "message": "Weather data update initiated",
        "status": "success",
        "timestamp": datetime.now().isoformat()
    })

@app.get("/update")
async def update_data_get(background_tasks: BackgroundTasks):
    """
    GET endpoint for updating data (redirects to homepage)
    """
    background_tasks.add_task(update_weather_data)
    
    html_content = """
    <html>
    <head>
        <title>Updating Weather Data</title>
        <meta http-equiv="refresh" content="3;url=/">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .loading { color: #667eea; font-size: 1.2em; }
        </style>
    </head>
    <body>
        <h1>🔄 Updating Weather Data</h1>
        <p class="loading">Please wait while we fetch fresh weather data...</p>
        <p>You will be redirected to the dashboard shortly.</p>
    </body>
    </html>
    """
    
    return HTMLResponse(html_content)

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data_available": cached_weather_data is not None,
        "last_update": last_update_time.isoformat() if last_update_time else None
    }

@app.get("/api/cities")
async def get_cities():
    """
    Get list of monitored cities
    """
    return {"cities": config.CITIES}

if __name__ == "__main__":
    print("🌤️ Starting Singular Weather Analytics Server")
    print(f"📊 Dashboard: http://{config.HOST}:{config.PORT}")
    print(f"📚 API Docs: http://{config.HOST}:{config.PORT}/docs")
    
    uvicorn.run(
        "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info"
    ) 