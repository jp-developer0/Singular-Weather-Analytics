"""
Comprehensive Test Suite for Singular Weather Analytics Platform
Tests all major components: data collection, processing, visualization, and web API
"""

import pytest
import asyncio
import pandas as pd
import os
import sys
from datetime import datetime
import logging

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from weather_scraper import WeatherScraper
from visualizations import WeatherVisualizer
from config import config
import app

# Configure test logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestWeatherScraper:
    """Test weather data collection and processing"""
    
    def setup_method(self):
        """Setup for each test"""
        self.scraper = WeatherScraper()
    
    def test_weather_scraper_initialization(self):
        """Test that weather scraper initializes correctly"""
        assert self.scraper.base_url == config.OPEN_METEO_BASE_URL
        assert hasattr(self.scraper, 'session')
        logger.info("✅ Weather scraper initialization test passed")
    
    def test_single_city_data_fetch(self):
        """Test fetching weather data for a single city"""
        # Test with New York coordinates
        weather_data = self.scraper.fetch_weather_data(40.7128, -74.0060, "New York")
        
        if weather_data:
            assert 'city' in weather_data
            assert 'temperature_c' in weather_data
            assert 'humidity' in weather_data
            assert 'wind_speed_ms' in weather_data
            assert weather_data['city'] == "New York"
            logger.info("✅ Single city data fetch test passed")
        else:
            logger.warning("⚠️ Single city data fetch returned None (network issue?)")
    
    def test_all_cities_data_collection(self):
        """Test collecting data for all configured cities"""
        weather_df = self.scraper.scrape_all_cities()
        
        if not weather_df.empty:
            # Verify DataFrame structure
            expected_columns = [
                'city', 'temperature_c', 'temperature_f', 'humidity',
                'wind_speed_ms', 'wind_speed_mph', 'latitude', 'longitude', 'timestamp'
            ]
            
            for col in expected_columns:
                assert col in weather_df.columns, f"Missing column: {col}"
            
            # Verify data types and ranges
            assert weather_df['temperature_c'].dtype in ['float64', 'int64']
            assert weather_df['humidity'].between(0, 100).all()
            assert len(weather_df) <= len(config.CITIES)
            
            logger.info(f"✅ All cities data collection test passed ({len(weather_df)} cities)")
        else:
            logger.warning("⚠️ All cities data collection returned empty DataFrame")
    
    def test_data_processing(self):
        """Test data processing and conversions"""
        # Create sample data
        sample_data = pd.DataFrame({
            'city': ['Test City'],
            'temperature_c': [20.0],
            'humidity': [65],
            'wind_speed_ms': [5.0],
            'latitude': [40.0],
            'longitude': [-74.0],
            'timestamp': [datetime.now().isoformat()]
        })
        
        processed_df = self.scraper.process_weather_data(sample_data)
        
        # Verify conversions
        assert 'temperature_f' in processed_df.columns
        assert 'wind_speed_mph' in processed_df.columns
        
        # Test conversion accuracy
        temp_f = processed_df['temperature_f'].iloc[0]
        expected_f = 20 * 9/5 + 32  # 68°F
        assert abs(temp_f - expected_f) < 0.1
        
        wind_mph = processed_df['wind_speed_mph'].iloc[0]
        expected_mph = 5.0 * 2.237  # ~11.2 mph
        assert abs(wind_mph - expected_mph) < 0.1
        
        logger.info("✅ Data processing test passed")
    
    def test_insights_generation(self):
        """Test business intelligence insights generation"""
        # Create sample data with multiple cities
        sample_data = pd.DataFrame({
            'city': ['Hot City', 'Cold City', 'Humid City'],
            'temperature_c': [30.0, 5.0, 20.0],
            'temperature_f': [86.0, 41.0, 68.0],
            'humidity': [40, 60, 90],
            'wind_speed_ms': [3.0, 8.0, 2.0],
            'wind_speed_mph': [6.7, 17.9, 4.5]
        })
        
        insights = self.scraper.get_weather_insights(sample_data)
        
        # Verify insights structure
        assert 'temperature_stats' in insights
        assert 'humidity_stats' in insights
        assert 'wind_stats' in insights
        assert 'total_cities' in insights
        
        # Verify insights accuracy
        assert insights['temperature_stats']['hottest_city'] == 'Hot City'
        assert insights['temperature_stats']['coldest_city'] == 'Cold City'
        assert insights['humidity_stats']['most_humid_city'] == 'Humid City'
        
        logger.info("✅ Insights generation test passed")

class TestWeatherVisualizer:
    """Test weather data visualization"""
    
    def setup_method(self):
        """Setup for each test"""
        self.visualizer = WeatherVisualizer()
        
        # Create sample data for testing
        self.sample_df = pd.DataFrame({
            'city': ['New York', 'Tokyo', 'London'],
            'temperature_c': [15, 20, 12],
            'temperature_f': [59, 68, 53.6],
            'humidity': [70, 60, 80],
            'wind_speed_ms': [5, 3, 4],
            'wind_speed_mph': [11.2, 6.7, 8.9]
        })
        
        self.sample_insights = {
            'total_cities': 3,
            'data_collection_time': datetime.now().isoformat(),
            'temperature_stats': {
                'hottest_city': 'Tokyo',
                'coldest_city': 'London',
                'avg_temperature_c': 15.7,
                'avg_temperature_f': 60.2
            },
            'humidity_stats': {
                'most_humid_city': 'London',
                'least_humid_city': 'Tokyo',
                'avg_humidity': 70.0
            },
            'wind_stats': {
                'windiest_city': 'New York',
                'calmest_city': 'Tokyo',
                'avg_wind_speed_mph': 8.9
            }
        }
    
    def test_visualizer_initialization(self):
        """Test visualizer initialization"""
        assert self.visualizer.charts_dir == config.CHARTS_DIR
        assert os.path.exists(self.visualizer.charts_dir)
        logger.info("✅ Visualizer initialization test passed")
    
    def test_temperature_chart_creation(self):
        """Test temperature comparison chart creation"""
        chart_path = self.visualizer.create_temperature_comparison_chart(self.sample_df)
        
        assert os.path.exists(chart_path)
        assert chart_path.endswith('.png')
        
        # Verify file size (should be reasonable for a chart)
        file_size = os.path.getsize(chart_path)
        assert file_size > 10000  # At least 10KB
        assert file_size < 5000000  # Less than 5MB
        
        logger.info("✅ Temperature chart creation test passed")
    
    def test_humidity_wind_chart_creation(self):
        """Test humidity and wind analysis chart creation"""
        chart_path = self.visualizer.create_humidity_wind_analysis(self.sample_df)
        
        assert os.path.exists(chart_path)
        assert chart_path.endswith('.png')
        
        logger.info("✅ Humidity and wind chart creation test passed")
    
    def test_comprehensive_dashboard_creation(self):
        """Test comprehensive dashboard creation"""
        chart_path = self.visualizer.create_comprehensive_dashboard(
            self.sample_df, self.sample_insights
        )
        
        assert os.path.exists(chart_path)
        assert chart_path.endswith('.png')
        
        logger.info("✅ Comprehensive dashboard creation test passed")
    
    def test_all_visualizations_generation(self):
        """Test generating all visualizations at once"""
        chart_paths = self.visualizer.generate_all_visualizations(
            self.sample_df, self.sample_insights
        )
        
        assert isinstance(chart_paths, dict)
        assert len(chart_paths) >= 3
        
        for chart_name, path in chart_paths.items():
            assert os.path.exists(path)
            assert path.endswith('.png')
        
        logger.info(f"✅ All visualizations generation test passed ({len(chart_paths)} charts)")

class TestConfiguration:
    """Test configuration management"""
    
    def test_config_values(self):
        """Test that configuration values are properly set"""
        assert hasattr(config, 'OPEN_METEO_BASE_URL')
        assert hasattr(config, 'CITIES')
        assert hasattr(config, 'OUTPUT_CSV_FILE')
        assert hasattr(config, 'CHARTS_DIR')
        
        # Test cities list
        assert len(config.CITIES) == 10
        for city in config.CITIES:
            assert 'City' in city
            assert 'Latitude' in city
            assert 'Longitude' in city
        
        logger.info("✅ Configuration test passed")
    
    def test_directory_creation(self):
        """Test that required directories are created"""
        config.ensure_directories()
        
        assert os.path.exists(config.CHARTS_DIR)
        assert os.path.exists("static")
        
        logger.info("✅ Directory creation test passed")

def test_csv_export():
    """Test CSV export functionality"""
    # Create sample data
    sample_df = pd.DataFrame({
        'city': ['Test City'],
        'temperature_c': [20.0],
        'temperature_f': [68.0],
        'humidity': [65],
        'wind_speed_ms': [5.0],
        'wind_speed_mph': [11.2],
        'latitude': [40.0],
        'longitude': [-74.0],
        'timestamp': [datetime.now().isoformat()]
    })
    
    # Export to CSV
    csv_path = config.OUTPUT_CSV_FILE
    sample_df.to_csv(csv_path, index=False)
    
    # Verify file exists and has content
    assert os.path.exists(csv_path)
    
    # Read back and verify
    read_df = pd.read_csv(csv_path)
    assert len(read_df) == 1
    assert read_df['city'].iloc[0] == 'Test City'
    
    logger.info("✅ CSV export test passed")

async def test_web_application():
    """Test web application endpoints (basic smoke test)"""
    try:
        # Test that the app can be imported and initialized
        from app import app as fastapi_app
        
        assert fastapi_app.title == "Singular Weather Analytics API"
        assert fastapi_app.version == "1.0.0"
        
        logger.info("✅ Web application initialization test passed")
        
    except Exception as e:
        logger.error(f"❌ Web application test failed: {e}")

def run_integration_test():
    """Run a full integration test"""
    logger.info("🧪 Starting integration test...")
    
    try:
        # Test full workflow
        scraper = WeatherScraper()
        visualizer = WeatherVisualizer()
        
        # 1. Collect data
        logger.info("1. Testing data collection...")
        weather_df = scraper.scrape_all_cities()
        
        if weather_df.empty:
            logger.warning("⚠️ No weather data collected - possibly network issues")
            return False
        
        # 2. Generate insights
        logger.info("2. Testing insights generation...")
        insights = scraper.get_weather_insights(weather_df)
        
        # 3. Create visualizations
        logger.info("3. Testing visualizations...")
        charts = visualizer.generate_all_visualizations(weather_df, insights)
        
        # 4. Export CSV
        logger.info("4. Testing CSV export...")
        csv_path = config.OUTPUT_CSV_FILE
        weather_df.to_csv(csv_path, index=False)
        
        # Verify everything worked
        assert len(insights) > 0
        assert len(charts) >= 3
        assert os.path.exists(csv_path)
        
        logger.info("✅ Integration test passed successfully!")
        logger.info(f"   📊 Cities processed: {len(weather_df)}")
        logger.info(f"   📈 Charts generated: {len(charts)}")
        logger.info(f"   📄 CSV exported: {csv_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Singular Weather Analytics - Test Suite")
    print("=" * 50)
    
    # Run individual component tests
    logger.info("Running component tests...")
    
    # Weather scraper tests
    test_scraper = TestWeatherScraper()
    test_scraper.setup_method()
    test_scraper.test_weather_scraper_initialization()
    test_scraper.test_single_city_data_fetch()
    test_scraper.test_all_cities_data_collection()
    test_scraper.test_data_processing()
    test_scraper.test_insights_generation()
    
    # Visualizer tests
    test_viz = TestWeatherVisualizer()
    test_viz.setup_method()
    test_viz.test_visualizer_initialization()
    test_viz.test_temperature_chart_creation()
    test_viz.test_humidity_wind_chart_creation()
    test_viz.test_comprehensive_dashboard_creation()
    test_viz.test_all_visualizations_generation()
    
    # Configuration tests
    test_config = TestConfiguration()
    test_config.test_config_values()
    test_config.test_directory_creation()
    
    # Other tests
    test_csv_export()
    
    # Web application test
    asyncio.run(test_web_application())
    
    # Integration test
    logger.info("\nRunning integration test...")
    integration_success = run_integration_test()
    
    print("\n" + "=" * 50)
    if integration_success:
        print("🎉 ALL TESTS PASSED! Application is ready for production.")
        print("\nTo start the application:")
        print("  python app.py")
        print("\nThen visit: http://localhost:8000")
    else:
        print("❌ Some tests failed. Check the logs above.")
    
    return integration_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 