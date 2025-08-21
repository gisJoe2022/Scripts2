
# water_backup.py
# This script creates a File Geodatabase and downloads various sewer-related feature services into it.
# It uses the ArcPy library to handle GIS data and operations.
# Author: J. Hayes
# date: 2025-08-01

import arcpy
import datetime
import os

arcpy.env.overwriteOutput = True  # Allow overwriting existing files

# Record the start time
start_time = datetime.datetime.now()

# Sign in to ArcGIS Online
portal_url = "https://bedfordvagis.maps.arcgis.com"
username = "j.hayes_bedfordvagis"
password = "letrbuck4EO!"
arcpy.SignInToPortal(portal_url, username, password)
print("Signed in to ArcGIS Online.")

# Set base directory where the geodatabase will be created
base_dir = r"S:\BU_Databases\2025\water"

# Create a name for the geodatabase using today's date
today_str = start_time.strftime('%Y%m%d_%H%M%S')
gdb_name = f"brwa_layers_backup_{today_str}.gdb"
gdb_path = os.path.join(base_dir, gdb_name)

# Create the File Geodatabase
arcpy.CreateFileGDB_management(base_dir, gdb_name)
print(f"Created File Geodatabase: {gdb_path}")

# List of ESRI-hosted feature service URLs
feature_services = [
    
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Hydrant_Lateral_BRWAVersion/FeatureServer/2",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Water_Lateral/FeatureServer/4460",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Waterline_BRWA_Version2021/FeatureServer/2",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Water_Pump_Station_2021/FeatureServer/2",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Low_Pressure_Zones_/FeatureServer/3",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Pressure_Tank/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Water_Tank_BRWA_Version/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Water_Treatment_Plant/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/ADU/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Manhole_Water/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Casing/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Water_Valve/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Vault_2021_02_12/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Fire_Hydrant_BRWA/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Water_Pump/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Abandoned_Water_Sewer_Lines/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Well/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Control_Box/FeatureServer/2",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Air_Release/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Blowoff/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Control_Valve/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Water_Meter_2021/FeatureServer/0",
"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/WLs_2in_below/FeatureServer/1969"
]

# Corresponding names for the output feature classes
output_names = [
    "hydrant_lateral",
    "water_lateral",
    "waterline_brwa_version",
    "water_pump_station",
    "low_pressure_zones",
    "pressure_tank",
    "water_tank_brwa_version",
    "water_treatment_plant",
    "adu",
    "manhole_water",
    "casing",
    "water_valve",
    "vault_2021_02_12",
    "fire_hydrant_brwa",
    "water_pump",
    "abandoned_water_sewer_lines",
    "well",
    "control_box",
    "air_release",
    "blowoff",
    "control_valve",
    "water_meter_2021",
    "wls_2in_below"
]

# Download and save each feature service into the geodatabase
for url, name in zip(feature_services, output_names):
    output_path = os.path.join(gdb_path, name)
    print(f"Downloading {name} from {url}...")
    arcpy.FeatureClassToFeatureClass_conversion(url, gdb_path, name)
    print(f"Saved to {output_path}")

# Record the end time and calculate duration
end_time = datetime.datetime.now()
duration = end_time - start_time
minutes, seconds = divmod(duration.total_seconds(), 60)
print(f"Script completed in {int(minutes)} minutes and {int(seconds)} seconds.")