# sewer_backup.py
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
base_dir = r"S:\BU_Databases\2025\sewer"

# Create a name for the geodatabase using today's date
today_str = start_time.strftime('%Y%m%d')
gdb_name = f"brwa_sewer_backup_{today_str}.gdb"
gdb_path = os.path.join(base_dir, gdb_name)

# Create the File Geodatabase
arcpy.CreateFileGDB_management(base_dir, gdb_name)
print(f"Created File Geodatabase: {gdb_path}")

# List of ESRI-hosted feature service URLs
feature_services = [
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Meter/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Fitting/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Omni_Marker/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_System_Valve/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Manhole/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Force_Main_Sewer_2020/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Gravity_Main_Sewer_2020/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Vault/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Pump_Station/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Cleanout_BRWA_2020/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Grinder_Pump/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Treatment_Plant/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Service_lateral_2021/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sub_DrainageAreas/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Emergency_Pump_Connection/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/sCasing/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Connection_Box/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Slope_Anchors/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Pump2/FeatureServer/2879",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Air_Valve/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Wet_Well/FeatureServer/2"
]

# Corresponding names for the output feature classes
output_names = [
    "sewer_meters",
    "Sewer_fittings",
    "omni_markers",
    "Sewer_system_valves",
    "Sewer_manhole",
    "force_main_sewer_2020",
    "gravity_main_sewer_2020",
    "Sewer_vaults",
    "Sewer_pump_stations",
    "cleanouts_brwa_2020",
    "grinder_pumps",
    "Sewer_treatment_plants",
    "Sewer_service_laterals_2021",
    "sub_drainage_areas",
    "Sewer_emergency_pump_connections",
    "sCasing",
    "Sewer_connection_boxes",
    "slope_anchors",
    "Sewer_pump2",
    "Sewer_air_valves",
    "wet_wells"
    
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


"""# sewer_backup.py
import arcpy
import datetime
import os

arcpy.env.overwriteOutput = True  # Allow overwriting existing files

# Sign in to ArcGIS Online
portal_url = "https://bedfordvagis.maps.arcgis.com"
username = "j.hayes_bedfordvagis"
password = "letrbuck4EO!"
arcpy.SignInToPortal(portal_url, username, password)
print("Signed in to ArcGIS Online.")


 # Set base directory where the geodatabase will be created
base_dir = r"S:\BU_Databases\2025"

# Create a name for the geodatabase using today's date
today_str = datetime.datetime.today().strftime('%Y%m%d')
gdb_name = f"brwa_backup_{today_str}.gdb"
gdb_path = os.path.join(base_dir, gdb_name)

# Create the File Geodatabase
arcpy.CreateFileGDB_management(base_dir, gdb_name)
print(f"Created File Geodatabase: {gdb_path}")

# Create the 'Sewer' feature dataset
feature_dataset = "Sewer"
spatial_reference = arcpy.SpatialReference(2284)  # NAD 1983 StatePlane Virginia South FIPS 4502 (US Feet)
arcpy.CreateFeatureDataset_management(gdb_path, feature_dataset, spatial_reference)
print(f"Created Feature Dataset: {feature_dataset}")

# List of ESRI-hosted feature service URLs
feature_services = [
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Meter/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Fitting/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Omni_Marker/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_System_Valve/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Manhole/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Force_Main_Sewer_2020/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Gravity_Main_Sewer_2020/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Vault/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Pump_Station/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Cleanout_BRWA_2020/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Grinder_Pump/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Treatment_Plant/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Service_lateral_2021/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sub_DrainageAreas/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Emergency_Pump_Connection/FeatureServer/0",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/sCasing/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Connection_Box/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Slope_Anchors/FeatureServer/2",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sewer_Pump2/FeatureServer/2879"

]

# Corresponding names for the output feature classes
output_names = [
    "sewer_meters",
    "Sewer_fittings",
    "omni_markers",
    "Sewer_system_valves",
    "Sewer_manhole",
    "force_main_sewer_2020",
    "gravity_main_sewer_2020",
    "Sewer_vaults",
    "Sewer_pump_stations",
    "cleanouts_brwa_2020",
    "grinder_pumps",
    "Sewer_treatment_plants",
    "Sewer_service_laterals_2021",
    "sub_drainage_areas",
    "Sewer_emergency_pump_connections",
    "sCasing",
    "Sewer_connection_boxes",
    "slope_anchors",
    "Sewer_pump2"
    
]

# Download and save each feature service into the Sewer feature dataset
for url, name in zip(feature_services, output_names):
    output_path = os.path.join(gdb_path, feature_dataset, name)
    print(f"Downloading {name} from {url}...")
    arcpy.FeatureClassToFeatureClass_conversion(url, os.path.join(gdb_path, feature_dataset), name)
    print(f"Saved to {output_path}")
    

    end_time = datetime.datetime.now()
    duration = end_time - datetime.datetime.strptime(today_str, '%Y%m%d')
   
    print(f"Script duration: {duration}")

print("All feature services have been downloaded and saved.")
 """