# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NAME: .py
# Description: Initiates a Get request to a REST service
# Purpose: Download publically available data.
# Author:      Joe Hayes
# Created:     3/22/2023
# ---------------------------------------------------------------------------

# modules
import arcpy

# Set environment settings
arcpy.env.overwriteOutput = True

arcpy.management.XYTableToPoint(r"C:\Users\josephh\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\psqlgis1_production_SURVEY.sde\production.survey.V_GPS", r"C:\Users\josephh\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\psqlgis1_production_SURVEY.sde\production.SURVEY.corner_GPS", "easting_f", "northing_f", None, 'PROJCS["NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601_Feet_Intl",GEOGCS["GCS_North_American_1983_HARN",DATUM["D_North_American_1983_HARN",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",8202099.737532808],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-120.5],PARAMETER["Standard_Parallel_1",44.33333333333334],PARAMETER["Standard_Parallel_2",46.0],PARAMETER["Latitude_Of_Origin",43.66666666666666],UNIT["Foot",0.3048]];-450359962737.049 -450359962737.049 10000;0 1;0 1;0.001;0.001;0.001;IsHighPrecision')

print('GPS points update complete')