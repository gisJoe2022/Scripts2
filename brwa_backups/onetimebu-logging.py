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
log_dir = r"S:\BU_Databases\Historical_datasets\logs"  # Change this to your desired log directory
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

    base_dir = r"S:\BU_Databases\Historical_datasets"
    today_str = start_time.strftime('%Y%m%d_%H%M')
    gdb_name = f"historical_backup_{today_str}.gdb"
    gdb_path = os.path.join(base_dir, gdb_name)

    arcpy.CreateFileGDB_management(base_dir, gdb_name)
    print(f"Created File Geodatabase: {gdb_path}")

    # List of ESRI-hosted feature service URLs
    feature_services = [
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/2019_Bedford_Town_SML_junctions/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/2019_Forest_Central_Stewartsville_junctions/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/2020_Bedford_Town_SML_Junctions/FeatureServer/4403",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/2020_Forest_Central_Stewartsville_junctions/FeatureServer/4404",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/2021_Available_Fire_Flow___Bedford_Town_and_SML/FeatureServer/4402",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/2021_Available_Fire_Flow___Forest_Central/FeatureServer/4401",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/2022_Forest_Model/FeatureServer/4397",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/2022_Town_junctions_Model/FeatureServer/4396",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Customer_Breakdown__Aug_2018_/FeatureServer/2",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/exstavff_2014/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/exstpress_2014/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Fire_Service_Boundary/FeatureServer/0",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Golf_Course/FeatureServer/0",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/juncavff___Central/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/juncpres___Cental/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Landscaping_Conflicts/FeatureServer/1",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Mariners_Irrigation/FeatureServer/1",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Model_Junctions___Available_Fire_Flow_2024/FeatureServer/4967",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Operations_/FeatureServer/5",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Operations_/FeatureServer/6",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Operations_/FeatureServer/7",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/PROPAVFF___Central/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/PRVs_Waterlines/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/RUN2AVFF_2016/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/RUN2AVFF_2017/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/RUN2PRES_2016/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/RUN2PRES_2017/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Stoney_Creek_Dam_Studies_/FeatureServer/3",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Stoney_Creek_Dam_Studies_/FeatureServer/4",
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Trace_Wire/FeatureServer/3"

    ]

    # Corresponding names for the output feature classes
    output_names = [
        "Bedford_Town_SML_junctions_2019",
        "Forest_Central_Stewartsville_junctions_2019",
        "Bedford_Town_SML_Junctions_2020",
        "Forest_Central_Stewartsville_junctions_2020",
        "Available_Fire_Flow_Bedford_Town_and_SML_2021",
        "Available_Fire_Flow_Forest_Central_2021",
        "Forest_Model_2022",
        "Town_junctions_Model_2022",
        "Customer_Breakdown_Aug_2018",
        "exstavff_2014",
        "exstpress_2014",
        "Fire_Service_Boundary",
        "Golf_Course",
        "juncavff_Central",
        "juncpres_Cental",
        "Landscaping_Conflicts",
        "Mariners_Irrigation",
        "Model_Junctions_Available_Fire_Flow_2024",
        "Operations_Valve_Locations",
        "Operations_Hydrants",
        "Operations_Meters",
        "PROPAVFF_Central",
        "PRVs_Waterlines",
        "RUN2AVFF_2016",
        "RUN2AVFF_2017",
        "RUN2PRES_2016",
        "RUN2PRES_2017",
        "Stoney_Creek_Dam_Studies_Junctions",
        "Stoney_Creek_Dam_Studies_Pipes",
        "Trace_Wire"
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