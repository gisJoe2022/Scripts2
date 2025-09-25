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
log_dir = r"S:\BU_Databases\2025\brwa_layers\logs"  # Change this to your desired log directory
os.makedirs(log_dir, exist_ok=True)  # Ensure the log directory exists
log_file = os.path.join(log_dir, f"brwa_brwa_backup_{timestamp}.log")

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

    base_dir = r"S:\BU_Databases\2025\brwa_layers"
    today_str = start_time.strftime('%Y%m%d_%H%M')
    gdb_name = f"brwa_layers_backup_{today_str}.gdb"
    gdb_path = os.path.join(base_dir, gdb_name)

    arcpy.CreateFileGDB_management(base_dir, gdb_name)
    print(f"Created File Geodatabase: {gdb_path}")

    # List of ESRI-hosted feature service URLs
    feature_services = [
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/BRWAHydrants/FeatureServer/0",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Buildings/FeatureServer/1735",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/CIP_Projects/FeatureServer/1",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Connects/FeatureServer/1",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Critical_Customers/FeatureServer/1",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Easement_Notes/FeatureServer/2",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Easements__Parcels_/FeatureServer/2",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Easements_2012/FeatureServer/2",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Fire_Flow_Records/FeatureServer/0",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Fire_Flow_Testing/FeatureServer/2",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Gas_Line/FeatureServer/1876",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Mandatory_Connection_Exceptions/FeatureServer/2",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Omni_Marker/FeatureServer/0",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/SGP_Installation_Verification_/FeatureServer/0",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Sureties/FeatureServer/0",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Survey_Points/FeatureServer/1",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/survey123_bf48dd2288e549969fbb51fdb4426ffe/FeatureServer/0",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/survey123_ed3e2ad4257b468abf394f06d221acbd_results/FeatureServer/1",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Trace_Wire_Box/FeatureServer/1",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/UGElectric/FeatureServer/1877",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Well_Permits/FeatureServer/2",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/WL_Projects/FeatureServer/3664"
    ]

    # Corresponding names for the output feature classes
    output_names = [
        "BRWAHydrants",
        "Buildings",
        "CIP_Projects",
        "Connects",
        "Critical_Customers",
        "Easements_Parcels",
        "Easements_2012",
        "Fire_Flow_Records",
        "Fire_Flow_Testing",
        "Gas_Line",
        "Mandatory_Connection_Exceptions",
        "Omni_Marker",
        "SGP_Installation_Verification",
        "Sureties",
        "Survey_Points",
        "survey123_1",
        "survey123_results",
        "Trace_Wire_Box",
        "UGElectric",
        "Well_Permits",
        "WL_Projects"
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