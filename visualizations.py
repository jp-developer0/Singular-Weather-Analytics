"""
Weather Data Visualization Module
Professional data visualization for Singular Analytics Platform
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
import os
from datetime import datetime
import logging
from config import config

# Configure logging
logger = logging.getLogger(__name__)

# Set the style for professional, business-ready visualizations
plt.style.use('default')
sns.set_palette("husl")

class WeatherVisualizer:
    """
    Professional weather data visualization suite
    Designed for analytics and business intelligence dashboards
    """
    
    def __init__(self):
        self.charts_dir = config.CHARTS_DIR
        self.figure_size = (12, 8)
        self.dpi = 300
        
        # Ensure charts directory exists
        os.makedirs(self.charts_dir, exist_ok=True)
        
        # Configure matplotlib for high-quality output
        plt.rcParams.update({
            'figure.dpi': self.dpi,
            'savefig.dpi': self.dpi,
            'font.size': 10,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'figure.titlesize': 16
        })
    
    def create_temperature_comparison_chart(self, df: pd.DataFrame) -> str:
        """
        Create a professional temperature comparison bar chart
        
        Args:
            df: Weather DataFrame with temperature data
            
        Returns:
            Path to the saved chart image
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Celsius chart
        bars1 = ax1.bar(df['city'], df['temperature_c'], 
                       color=sns.color_palette("coolwarm", len(df)))
        ax1.set_title('Temperature Comparison (Celsius)', fontweight='bold', pad=20)
        ax1.set_xlabel('Cities')
        ax1.set_ylabel('Temperature (°C)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}°C', ha='center', va='bottom', fontweight='bold')
        
        # Fahrenheit chart
        bars2 = ax2.bar(df['city'], df['temperature_f'], 
                       color=sns.color_palette("coolwarm", len(df)))
        ax2.set_title('Temperature Comparison (Fahrenheit)', fontweight='bold', pad=20)
        ax2.set_xlabel('Cities')
        ax2.set_ylabel('Temperature (°F)')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}°F', ha='center', va='bottom', fontweight='bold')
        
        plt.suptitle('Global Weather Temperature Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save chart
        chart_path = os.path.join(self.charts_dir, 'temperature_comparison.png')
        plt.savefig(chart_path, bbox_inches='tight', dpi=self.dpi)
        plt.close()
        
        logger.info(f"Temperature comparison chart saved to {chart_path}")
        return chart_path
    
    def create_humidity_wind_analysis(self, df: pd.DataFrame) -> str:
        """
        Create humidity and wind speed analysis charts
        
        Args:
            df: Weather DataFrame
            
        Returns:
            Path to the saved chart image
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Humidity bar chart
        bars1 = ax1.bar(df['city'], df['humidity'], 
                       color=sns.color_palette("Blues_r", len(df)))
        ax1.set_title('Humidity Levels by City', fontweight='bold')
        ax1.set_xlabel('Cities')
        ax1.set_ylabel('Humidity (%)')
        ax1.tick_params(axis='x', rotation=45)
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.0f}%', ha='center', va='bottom', fontweight='bold')
        
        # Wind speed bar chart (mph)
        bars2 = ax2.bar(df['city'], df['wind_speed_mph'], 
                       color=sns.color_palette("Greens", len(df)))
        ax2.set_title('Wind Speed by City (mph)', fontweight='bold')
        ax2.set_xlabel('Cities')
        ax2.set_ylabel('Wind Speed (mph)')
        ax2.tick_params(axis='x', rotation=45)
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Humidity vs Temperature scatter plot
        scatter = ax3.scatter(df['temperature_c'], df['humidity'], 
                            s=100, c=df['wind_speed_mph'], cmap='viridis', alpha=0.7)
        ax3.set_title('Temperature vs Humidity (colored by Wind Speed)', fontweight='bold')
        ax3.set_xlabel('Temperature (°C)')
        ax3.set_ylabel('Humidity (%)')
        
        # Add city labels to scatter plot
        for i, city in enumerate(df['city']):
            ax3.annotate(city, (df['temperature_c'].iloc[i], df['humidity'].iloc[i]),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        # Add colorbar for wind speed
        cbar = plt.colorbar(scatter, ax=ax3)
        cbar.set_label('Wind Speed (mph)')
        
        # Wind speed distribution
        ax4.hist(df['wind_speed_mph'], bins=8, color='skyblue', alpha=0.7, edgecolor='black')
        ax4.set_title('Wind Speed Distribution', fontweight='bold')
        ax4.set_xlabel('Wind Speed (mph)')
        ax4.set_ylabel('Number of Cities')
        ax4.axvline(df['wind_speed_mph'].mean(), color='red', linestyle='--', 
                   label=f'Average: {df["wind_speed_mph"].mean():.1f} mph')
        ax4.legend()
        
        plt.suptitle('Weather Analytics Dashboard - Humidity & Wind Analysis', 
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save chart
        chart_path = os.path.join(self.charts_dir, 'humidity_wind_analysis.png')
        plt.savefig(chart_path, bbox_inches='tight', dpi=self.dpi)
        plt.close()
        
        logger.info(f"Humidity and wind analysis chart saved to {chart_path}")
        return chart_path
    
    def create_comprehensive_dashboard(self, df: pd.DataFrame, insights: Dict) -> str:
        """
        Create a comprehensive weather dashboard with key metrics
        
        Args:
            df: Weather DataFrame
            insights: Weather insights dictionary
            
        Returns:
            Path to the saved dashboard image
        """
        fig = plt.figure(figsize=(20, 12))
        
        # Create a grid layout
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # Main temperature chart
        ax1 = fig.add_subplot(gs[0, :2])
        bars = ax1.bar(df['city'], df['temperature_c'], 
                      color=plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(df))))
        ax1.set_title('Global Temperature Overview (°C)', fontweight='bold', fontsize=14)
        ax1.tick_params(axis='x', rotation=45)
        ax1.set_ylabel('Temperature (°C)')
        
        # Add temperature values on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}°', ha='center', va='bottom', fontweight='bold')
        
        # Humidity pie chart (top cities)
        ax2 = fig.add_subplot(gs[0, 2])
        top_humid = df.nlargest(5, 'humidity')
        ax2.pie(top_humid['humidity'], labels=top_humid['city'], autopct='%1.1f%%',
               startangle=90, colors=sns.color_palette("Blues", 5))
        ax2.set_title('Top 5 Most Humid Cities', fontweight='bold')
        
        # Wind speed radar chart simulation
        ax3 = fig.add_subplot(gs[0, 3])
        ax3.bar(range(len(df)), df['wind_speed_mph'], 
               color=sns.color_palette("Greens", len(df)))
        ax3.set_title('Wind Speed (mph)', fontweight='bold')
        ax3.set_xticks(range(len(df)))
        ax3.set_xticklabels([city[:3] for city in df['city']], rotation=45)
        
        # Temperature vs Humidity scatter
        ax4 = fig.add_subplot(gs[1, :2])
        scatter = ax4.scatter(df['temperature_c'], df['humidity'], 
                            s=df['wind_speed_mph']*20, 
                            c=df['temperature_c'], cmap='RdYlBu_r', alpha=0.6)
        ax4.set_xlabel('Temperature (°C)')
        ax4.set_ylabel('Humidity (%)')
        ax4.set_title('Temperature vs Humidity (bubble size = wind speed)', fontweight='bold')
        
        # Add city labels
        for i, city in enumerate(df['city']):
            ax4.annotate(city, (df['temperature_c'].iloc[i], df['humidity'].iloc[i]),
                        xytext=(3, 3), textcoords='offset points', fontsize=8)
        
        # Key insights text box
        ax5 = fig.add_subplot(gs[1, 2:])
        ax5.axis('off')
        
        insights_text = f"""
KEY WEATHER INSIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌡️  TEMPERATURE ANALYSIS
   Hottest: {insights['temperature_stats']['hottest_city']}
   Coldest: {insights['temperature_stats']['coldest_city']}
   Average: {insights['temperature_stats']['avg_temperature_c']}°C

💧 HUMIDITY ANALYSIS  
   Most Humid: {insights['humidity_stats']['most_humid_city']}
   Least Humid: {insights['humidity_stats']['least_humid_city']}
   Average: {insights['humidity_stats']['avg_humidity']}%

🌪️  WIND ANALYSIS
   Windiest: {insights['wind_stats']['windiest_city']}
   Calmest: {insights['wind_stats']['calmest_city']}
   Average: {insights['wind_stats']['avg_wind_speed_mph']} mph

📊 DATA QUALITY
   Cities Analyzed: {insights['total_cities']}
   Collection Time: {insights['data_collection_time'][:19]}
        """
        
        ax5.text(0.05, 0.95, insights_text, transform=ax5.transAxes, fontsize=11,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
        
        # Bottom charts - distributions
        ax6 = fig.add_subplot(gs[2, 0])
        ax6.hist(df['temperature_c'], bins=6, color='orange', alpha=0.7, edgecolor='black')
        ax6.set_title('Temperature Distribution', fontweight='bold')
        ax6.set_xlabel('Temperature (°C)')
        
        ax7 = fig.add_subplot(gs[2, 1])
        ax7.hist(df['humidity'], bins=6, color='lightblue', alpha=0.7, edgecolor='black')
        ax7.set_title('Humidity Distribution', fontweight='bold')
        ax7.set_xlabel('Humidity (%)')
        
        ax8 = fig.add_subplot(gs[2, 2])
        ax8.hist(df['wind_speed_mph'], bins=6, color='lightgreen', alpha=0.7, edgecolor='black')
        ax8.set_title('Wind Speed Distribution', fontweight='bold')
        ax8.set_xlabel('Wind Speed (mph)')
        
        # Summary stats table
        ax9 = fig.add_subplot(gs[2, 3])
        ax9.axis('off')
        
        stats_data = [
            ['Metric', 'Min', 'Max', 'Avg'],
            ['Temp (°C)', f"{df['temperature_c'].min():.1f}", 
             f"{df['temperature_c'].max():.1f}", f"{df['temperature_c'].mean():.1f}"],
            ['Humidity (%)', f"{df['humidity'].min():.0f}", 
             f"{df['humidity'].max():.0f}", f"{df['humidity'].mean():.1f}"],
            ['Wind (mph)', f"{df['wind_speed_mph'].min():.1f}", 
             f"{df['wind_speed_mph'].max():.1f}", f"{df['wind_speed_mph'].mean():.1f}"]
        ]
        
        table = ax9.table(cellText=stats_data[1:], colLabels=stats_data[0],
                         cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)
        ax9.set_title('Summary Statistics', fontweight='bold')
        
        # Main title
        fig.suptitle('🌤️ Singular Weather Analytics Dashboard - Global Weather Intelligence', 
                     fontsize=18, fontweight='bold', y=0.98)
        
        # Save dashboard
        dashboard_path = os.path.join(self.charts_dir, 'weather_dashboard.png')
        plt.savefig(dashboard_path, bbox_inches='tight', dpi=self.dpi)
        plt.close()
        
        logger.info(f"Comprehensive weather dashboard saved to {dashboard_path}")
        return dashboard_path
    
    def generate_all_visualizations(self, df: pd.DataFrame, insights: Dict) -> Dict[str, str]:
        """
        Generate all weather visualizations
        
        Args:
            df: Weather DataFrame
            insights: Weather insights dictionary
            
        Returns:
            Dictionary mapping chart names to file paths
        """
        logger.info("Generating comprehensive weather visualizations")
        
        chart_paths = {}
        
        try:
            # Generate all charts
            chart_paths['temperature_comparison'] = self.create_temperature_comparison_chart(df)
            chart_paths['humidity_wind_analysis'] = self.create_humidity_wind_analysis(df)
            chart_paths['comprehensive_dashboard'] = self.create_comprehensive_dashboard(df, insights)
            
            logger.info(f"Successfully generated {len(chart_paths)} visualizations")
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
            
        return chart_paths

def main():
    """
    Main function for standalone testing of visualizations
    """
    print("📊 Singular Weather Visualizations - Testing Mode")
    
    # Create sample data for testing
    sample_data = {
        'city': ['New York', 'Tokyo', 'London', 'Paris', 'Berlin'],
        'temperature_c': [10, 15, 12, 8, 5],
        'temperature_f': [50, 59, 53.6, 46.4, 41],
        'humidity': [80, 60, 70, 85, 75],
        'wind_speed_ms': [5, 3, 4, 6, 7],
        'wind_speed_mph': [11.2, 6.7, 8.9, 13.4, 15.7]
    }
    
    df = pd.DataFrame(sample_data)
    
    sample_insights = {
        'total_cities': 5,
        'data_collection_time': datetime.now().isoformat(),
        'temperature_stats': {
            'hottest_city': 'Tokyo',
            'coldest_city': 'Berlin',
            'avg_temperature_c': 10.0,
            'avg_temperature_f': 50.0
        },
        'humidity_stats': {
            'most_humid_city': 'Paris',
            'least_humid_city': 'Tokyo',
            'avg_humidity': 74.0
        },
        'wind_stats': {
            'windiest_city': 'Berlin',
            'calmest_city': 'Tokyo',
            'avg_wind_speed_mph': 11.2
        }
    }
    
    visualizer = WeatherVisualizer()
    charts = visualizer.generate_all_visualizations(df, sample_insights)
    
    print(f"✅ Generated {len(charts)} test visualizations:")
    for name, path in charts.items():
        print(f"  • {name}: {path}")

if __name__ == "__main__":
    main() 