# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 09:55:39 2024

@author: ASUS
"""

import geopandas as gpd
from shapely.geometry import Point, MultiPolygon, Polygon
import pandas as pd


# Load the shapefile
shapefile_path = r'D:\OneDrive - UNIVERSITAS INDONESIA\Inventarisasi\GIS Inventarisasi Ciliwung\LU_SEG67.shp'
gdf = gpd.read_file(shapefile_path)

# Lists to store the points, their LU_IDs, and whether they are northernmost or southernmost
points = []
ids = []
extremes = []

# Iterate through each geometry (polygon) in the GeoDataFrame
for idx, row in gdf.iterrows():
    geom = row.geometry
    lu_id = row['LU_ID']  # Adjust this if the attribute name is different
    
    if geom.geom_type == 'Polygon':
        # Get the northernmost and southernmost points of the current polygon
        northernmost = max(geom.exterior.coords, key=lambda x: x[1])
        southernmost = min(geom.exterior.coords, key=lambda x: x[1])
        
        # Add points, LU_IDs, and extreme type to the lists
        points.append(Point(northernmost))
        ids.append(lu_id)
        extremes.append('northernmost')
        
        points.append(Point(southernmost))
        ids.append(lu_id)
        extremes.append('southernmost')
        
    elif geom.geom_type == 'MultiPolygon':
        for poly in geom.geoms:
            northernmost = max(poly.exterior.coords, key=lambda x: x[1])
            southernmost = min(poly.exterior.coords, key=lambda x: x[1])
            
            # Add points, LU_IDs, and extreme type to the lists
            points.append(Point(northernmost))
            ids.append(lu_id)
            extremes.append('northernmost')
            
            points.append(Point(southernmost))
            ids.append(lu_id)
            extremes.append('southernmost')

# Create a GeoDataFrame for the points with LU_IDs and extreme type
points_gdf = gpd.GeoDataFrame({'geometry': points, 'LU_ID': ids, 'Extreme_Type': extremes}, crs=gdf.crs)



# Save the points to a new shapefile
output_shapefile_path = r'D:\OneDrive - UNIVERSITAS INDONESIA\Inventarisasi\GIS Inventarisasi Ciliwung\points.shp'
points_gdf.to_file(output_shapefile_path)

print(f"Northernmost and southernmost points have been exported to {output_shapefile_path}")
