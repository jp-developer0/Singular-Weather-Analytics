"""
Singular Weather Analytics Web Application
Professional FastAPI application for weather data analytics and visualization
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, Response
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
        return templates.TemplateResponse("error.html", {"request": request})
    
    # Generate table rows for template
    table_rows = _generate_table_rows(cached_weather_data)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "insights": cached_insights,
        "last_update_time": last_update_time,
        "table_rows": table_rows
    })

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
async def get_weather_data_page(request: Request):
    """
    Weather data viewer page with navigation
    """
    if cached_weather_data is None:
        raise HTTPException(status_code=503, detail="Weather data not available")
    
    # Generate formatted data table
    def generate_json_table(data, title):
        if isinstance(data, dict):
            rows = ""
            for key, value in data.items():
                if isinstance(value, dict):
                    nested_table = generate_json_table(value, key)
                    rows += f"<tr><td class='key'>{key}</td><td>{nested_table}</td></tr>"
                elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                    # Table for list of objects
                    if key == "data":  # Main weather data
                        table_html = "<table class='data-table'><thead><tr>"
                        if value:
                            for col in value[0].keys():
                                table_html += f"<th>{col}</th>"
                            table_html += "</tr></thead><tbody>"
                            for row in value:
                                table_html += "<tr>"
                                for col_val in row.values():
                                    formatted_val = f"{col_val:.2f}" if isinstance(col_val, float) else str(col_val)
                                    table_html += f"<td>{formatted_val}</td>"
                                table_html += "</tr>"
                            table_html += "</tbody></table>"
                        rows += f"<tr><td class='key'>{key}</td><td>{table_html}</td></tr>"
                    else:
                        rows += f"<tr><td class='key'>{key}</td><td class='value'>{str(value)}</td></tr>"
                else:
                    formatted_value = f"{value:.2f}" if isinstance(value, float) else str(value)
                    rows += f"<tr><td class='key'>{key}</td><td class='value'>{formatted_value}</td></tr>"
            return f"<table class='json-table'><tbody>{rows}</tbody></table>"
        return str(data)
    
    weather_data = {
        "data": cached_weather_data.to_dict('records'),
        "insights": cached_insights,
        "last_updated": last_update_time.isoformat() if last_update_time else None,
        "total_cities": len(cached_weather_data)
    }
    
    data_table = generate_json_table(weather_data, "Weather Data")
    
    return templates.TemplateResponse("api_data.html", {
        "request": request,
        "last_update_time": last_update_time,
        "total_cities": len(cached_weather_data),
        "data_table": data_table
    })

@app.get("/api/data/raw")
async def get_weather_data_raw():
    """
    API endpoint to get current weather data as raw JSON
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
async def get_chart(chart_name: str, request: Request):
    """
    Serve weather visualization charts with navigation
    """
    if cached_charts is None or chart_name not in cached_charts:
        raise HTTPException(status_code=404, detail="Chart not found")
    
    chart_path = cached_charts[chart_name]
    
    if not os.path.exists(chart_path):
        raise HTTPException(status_code=404, detail="Chart file not found")
    
    # Chart titles mapping
    chart_titles = {
        "temperature_comparison": "📊 Temperature Comparison",
        "humidity_wind_analysis": "💨 Humidity & Wind Analysis", 
        "comprehensive_dashboard": "🎯 Comprehensive Dashboard"
    }
    
    chart_title = chart_titles.get(chart_name, "📈 Weather Chart")
    
    return templates.TemplateResponse("chart_view.html", {
        "request": request,
        "chart_name": chart_name,
        "chart_title": chart_title
    })

@app.get("/charts/raw/{chart_name}")
async def get_raw_chart(chart_name: str):
    """
    Serve raw chart image files
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
async def update_data_get(background_tasks: BackgroundTasks, request: Request):
    """
    GET endpoint for updating data (redirects to homepage)
    """
    background_tasks.add_task(update_weather_data)
    
    return templates.TemplateResponse("loading.html", {"request": request})

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

@app.get("/favicon.ico")
async def favicon():
    """
    Serve favicon to prevent 404 errors
    """
    # Simple weather-themed favicon (cloud emoji as SVG)
    favicon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
        <circle cx="30" cy="30" r="20" fill="#87CEEB" opacity="0.8"/>
        <circle cx="50" cy="25" r="25" fill="#B0E0E6" opacity="0.9"/>
        <circle cx="70" cy="30" r="18" fill="#87CEEB" opacity="0.8"/>
        <ellipse cx="50" cy="45" rx="35" ry="15" fill="#E6F3FF"/>
    </svg>"""
    
    return Response(
        content=favicon_svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": "max-age=86400"}  # Cache for 24 hours
    )

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