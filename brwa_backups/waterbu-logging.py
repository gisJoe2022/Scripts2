# sewer_backup.py
# This script creates a File Geodatabase and downloads various sewer-related feature services into it.
# It uses the ArcPy library to handle GIS data and operations.
# Author: J. Hayes
# date: 2025-08-01

import arcpy
import datetime
import os
import logging
import sys

# === Setup Logging ===
start_time = datetime.datetime.now()
timestamp = start_time.strftime('%Y%m%d_%H%M')
log_dir = r"S:\BU_Databases\2025\water\logs"  # Change this to your desired log directory
os.makedirs(log_dir, exist_ok=True)  # Ensure the log directory exists
log_file = os.path.join(log_dir, f"brwa_sewer_backup_{timestamp}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Redirect stdout and stderr to the log file
class StreamToLogger:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
    def write(self, message):
        if message.strip():
            self.logger.log(self.level, message.strip())
    def flush(self):
        pass

sys.stdout = StreamToLogger(logging.getLogger(), logging.INFO)
sys.stderr = StreamToLogger(logging.getLogger(), logging.ERROR)

# === Script Begins ===
try:
    arcpy.env.overwriteOutput = True
    print("Script started.")

    portal_url = "https://bedfordvagis.maps.arcgis.com"
    username = "brwa.sync_bedfordvagis"
    password = "E&MBp^U@)4ybMWq"
    arcpy.SignInToPortal(portal_url, username, password)
    print("Signed in to ArcGIS Online.")

    base_dir = r"S:\BU_Databases\2025\water"
    today_str = start_time.strftime('%Y%m%d_%H%M')
    gdb_name = f"brwa_sewer_backup_{today_str}.gdb"
    gdb_path = os.path.join(base_dir, gdb_name)

    arcpy.CreateFileGDB_management(base_dir, gdb_name)
    print(f"Created File Geodatabase: {gdb_path}")

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
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Blowoff/FeatureServer/0",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Control_Valve/FeatureServer/0",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Water_Meter_2021/FeatureServer/0"
    ]

    # Corresponding names for the output feature classes
    output_names = [
        "hydrant_lateral",
        "water_lateral",
        "waterline_brwa_version2021",
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
        "blowoff",
        "control_valve",
        "water_meter_2021"
    ]

    for url, name in zip(feature_services, output_names):
        output_path = os.path.join(gdb_path, name)
        print(f"Downloading {name} from {url}...")
        arcpy.FeatureClassToFeatureClass_conversion(url, gdb_path, name)
        print(f"Saved to {output_path}")

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    minutes, seconds = divmod(duration.total_seconds(), 60)
    print(f"Script completed in {int(minutes)} minutes and {int(seconds)} seconds.")

except Exception as e:
    logging.exception("An error occurred during script execution.")
    print(f"An error occurred: {e}")