import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path

def clean_column_names(columns):
    """
    Function to clean column names:
    - Convert to lowercase
    - Replace spaces and special characters with underscores
    """
    cleaned_columns = [col.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_') for col in columns]
    return cleaned_columns

# Define file paths using Path objects
raw_data_path = Path('data/raw/crash_injuries_fatalities_2018-01-01_2023-12-11.csv')
intermediate_data_path = Path('data/intermediate/crash_data.geojson')
# data/raw/crash_injuries_fatalities_2018-01-01_2023-12-11.csv
# Load the data
df = pd.read_csv(raw_data_path)

# Clean column names
df.columns = clean_column_names(df.columns)

# Data Cleaning
# Replace '*' and 'N/A' with NaN
df.replace(['*', 'N/A'], [None, None], inplace=True)

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(
    df, 
    geometry=gpd.points_from_xy(df['longitude_generated'], df['latitude_generated']),
    crs='EPSG:4326'
)

# Write to GeoJSON
gdf.to_file(intermediate_data_path, driver='GeoJSON')
