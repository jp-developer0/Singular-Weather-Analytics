"""
Weather Data Scraper Module
Professional weather data collection and processing for Singular Analytics
"""

import requests
import pandas as pd
import time
from typing import List, Dict, Optional
import logging
from datetime import datetime
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherScraper:
    """
    Professional weather data scraper using Open-Meteo API
    Designed for analytics and business intelligence applications
    """
    
    def __init__(self):
        self.base_url = config.OPEN_METEO_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Singular-Weather-Analytics/1.0'
        })
    
    def fetch_weather_data(self, latitude: float, longitude: float, city_name: str) -> Optional[Dict]:
        """
        Fetch current weather data for a specific location
        
        Args:
            latitude: City latitude
            longitude: City longitude
            city_name: Name of the city for logging
            
        Returns:
            Dictionary with weather data or None if failed
        """
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current_weather': 'true',
                'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m',
                'forecast_days': 1
            }
            
            logger.info(f"Fetching weather data for {city_name}")
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            current_weather = data.get('current_weather', {})
            hourly = data.get('hourly', {})
            
            # Get the first hourly reading for humidity (current_weather doesn't include humidity)
            humidity = None
            if hourly.get('relative_humidity_2m') and len(hourly['relative_humidity_2m']) > 0:
                humidity = hourly['relative_humidity_2m'][0]
            
            return {
                'city': city_name,
                'latitude': latitude,
                'longitude': longitude,
                'temperature_c': current_weather.get('temperature'),
                'humidity': humidity,
                'wind_speed_ms': current_weather.get('windspeed'),
                'timestamp': current_weather.get('time', datetime.now().isoformat())
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {city_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {city_name}: {e}")
            return None
    
    def scrape_all_cities(self, cities: List[Dict] = None) -> pd.DataFrame:
        """
        Scrape weather data for all cities and return processed DataFrame
        
        Args:
            cities: List of city dictionaries with Latitude, Longitude, City keys
                   If None, uses default cities from config
        
        Returns:
            Processed pandas DataFrame with weather data
        """
        if cities is None:
            cities = config.CITIES
        
        weather_data = []
        
        for city_info in cities:
            city_name = city_info['City']
            latitude = city_info['Latitude']
            longitude = city_info['Longitude']
            
            # Fetch weather data
            weather = self.fetch_weather_data(latitude, longitude, city_name)
            if weather:
                weather_data.append(weather)
            
            # Rate limiting - be respectful to the API
            time.sleep(0.1)
        
        if not weather_data:
            logger.error("No weather data collected")
            return pd.DataFrame()
        
        # Create DataFrame
        df = pd.DataFrame(weather_data)
        
        # Process the data
        return self.process_weather_data(df)
    
    def process_weather_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process raw weather data with conversions and analytics
        
        Args:
            df: Raw weather DataFrame
            
        Returns:
            Processed DataFrame with additional calculated fields
        """
        if df.empty:
            return df
        
        logger.info("Processing weather data with conversions and analytics")
        
        # Temperature conversion: Celsius to Fahrenheit
        df['temperature_f'] = df['temperature_c'] * 9/5 + 32
        
        # Wind speed conversion: m/s to mph
        df['wind_speed_mph'] = df['wind_speed_ms'] * 2.237
        
        # Round values for better presentation
        df['temperature_c'] = df['temperature_c'].round(1)
        df['temperature_f'] = df['temperature_f'].round(1)
        df['wind_speed_ms'] = df['wind_speed_ms'].round(1)
        df['wind_speed_mph'] = df['wind_speed_mph'].round(1)
        
        # Reorder columns for better readability
        column_order = [
            'city', 'temperature_c', 'temperature_f', 'humidity', 
            'wind_speed_ms', 'wind_speed_mph', 'latitude', 'longitude', 'timestamp'
        ]
        
        df = df[column_order]
        
        # Sort by temperature (descending) for analytics insights
        df = df.sort_values('temperature_c', ascending=False).reset_index(drop=True)
        
        logger.info(f"Successfully processed weather data for {len(df)} cities")
        return df
    
    def get_weather_insights(self, df: pd.DataFrame) -> Dict:
        """
        Generate business intelligence insights from weather data
        Perfect for Singular's analytics focus
        
        Args:
            df: Processed weather DataFrame
            
        Returns:
            Dictionary with key insights and statistics
        """
        if df.empty:
            return {}
        
        insights = {
            'total_cities': len(df),
            'data_collection_time': datetime.now().isoformat(),
            'temperature_stats': {
                'hottest_city': df.loc[df['temperature_c'].idxmax(), 'city'],
                'coldest_city': df.loc[df['temperature_c'].idxmin(), 'city'],
                'avg_temperature_c': df['temperature_c'].mean().round(1),
                'avg_temperature_f': df['temperature_f'].mean().round(1)
            },
            'humidity_stats': {
                'most_humid_city': df.loc[df['humidity'].idxmax(), 'city'],
                'least_humid_city': df.loc[df['humidity'].idxmin(), 'city'],
                'avg_humidity': df['humidity'].mean().round(1)
            },
            'wind_stats': {
                'windiest_city': df.loc[df['wind_speed_mph'].idxmax(), 'city'],
                'calmest_city': df.loc[df['wind_speed_mph'].idxmin(), 'city'],
                'avg_wind_speed_mph': df['wind_speed_mph'].mean().round(1)
            }
        }
        
        return insights

def main():
    """
    Main function for standalone execution
    Demonstrates the weather scraping capabilities
    """
    print("🌤️  Singular Weather Analytics - Data Collection Started")
    print("=" * 60)
    
    scraper = WeatherScraper()
    
    # Scrape weather data
    weather_df = scraper.scrape_all_cities()
    
    if weather_df.empty:
        print("❌ No weather data could be collected")
        return
    
    # Display results
    print(f"\n✅ Successfully collected weather data for {len(weather_df)} cities")
    print("\n📊 Weather Data Summary:")
    print(weather_df.to_string(index=False))
    
    # Generate insights
    insights = scraper.get_weather_insights(weather_df)
    print(f"\n🎯 Key Insights:")
    print(f"• Hottest: {insights['temperature_stats']['hottest_city']}")
    print(f"• Coldest: {insights['temperature_stats']['coldest_city']}")
    print(f"• Most Humid: {insights['humidity_stats']['most_humid_city']}")
    print(f"• Windiest: {insights['wind_stats']['windiest_city']}")
    
    # Export to CSV
    csv_file = config.OUTPUT_CSV_FILE
    weather_df.to_csv(csv_file, index=False)
    print(f"\n💾 Data exported to: {csv_file}")

if __name__ == "__main__":
    main() 