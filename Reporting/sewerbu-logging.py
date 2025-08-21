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
log_dir = r"\\nu\GIS\BU_Databases\scripts\scheduled_tasks\script_sewer\logs"  # Change this to your desired log directory
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

    base_dir = r"S:\BU_Databases\2025\sewer"
    today_str = start_time.strftime('%Y%m%d')
    gdb_name = f"brwa_sewer_backup_{today_str}.gdb"
    gdb_path = os.path.join(base_dir, gdb_name)

    arcpy.CreateFileGDB_management(base_dir, gdb_name)
    print(f"Created File Geodatabase: {gdb_path}")

    feature_services = [ ... ]  # Keep your list of URLs here
    output_names = [ ... ]      # Keep your list of output names here

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
