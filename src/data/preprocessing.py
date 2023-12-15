import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
from janitor import clean_names

# Define file paths using Path objects
raw_data_path = Path("data/raw/crash_injuries_fatalities_2018-01-01_2023-12-11.csv")
intermediate_data_path = Path("data/intermediate/crash_data.geojson")
clean_data_path = Path("data/clean/crash_data.geojson")
city_council_district_geojson_path = Path("data/raw/city_council_districts.geojson")

# Load the data and rename df to crash_data
crash_data = pd.read_csv(raw_data_path)

# Clean column names
crash_data = clean_names(crash_data)

# Replace '*' and 'N/A' with NaN
crash_data.replace(["*", "N/A"], [None, None], inplace=True)

# Create a variable for non-motorist involved crashes
crash_data["non_motorist_involved"] = crash_data["nonmotoristid"].notna()

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(
    crash_data,
    geometry=gpd.points_from_xy(crash_data["longitude_generated_"], crash_data["latitude_generated_"]),
    crs="EPSG:4326",
)

# Read in and clean city council district data
city_council_districts = gpd.read_file(city_council_district_geojson_path)
# Make sure the crs is the same as the crash data
city_council_districts = city_council_districts.to_crs("EPSG:4326")
city_council_districts = clean_names(city_council_districts)
city_council_districts.rename(
    columns={"area_name": "district", "cntct_nme": "council_member"}, inplace=True
)

# Perform spatial join to get city council district for each crash
gdf = gpd.sjoin(
    gdf,
    city_council_districts[["geometry", "district", "council_member"]],
    how="left",
    op="within",
)
# print the columns to make sure the join worked
# print("Columns:", gdf.columns)
cols =  [
        "reportnumber",
        "circumstancescode",
        "non_motorist_involved",
        "district",
        "council_member",
        "geometry",
    ]

gdf = gdf[cols]
# Write to GeoJSON
gdf.to_file(clean_data_path, driver="GeoJSON")
# Write city_council_districts to GeoJSON
city_council_districts.to_file(
    "data/clean/city_council_districts.geojson", driver="GeoJSON"
)
print("Done!")
