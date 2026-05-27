# ------------------------------------------------------------------
# PIPE UPDATE SCRIPT
# This script appends data from Force Main Sewer, Gravity Main Sewer, 
# and Water Main feature classes into a combined feature class called 
# "Combined Pipes". It also calculates the "Type" field for each record based on the source feature class.
# The script logs each step of the process, including successes and errors, into a CSV file for auditing purposes.
# Joe Hayes - 05/07/2026
# ------------------------------------------------------------------    


# ==================================================================
# IMPORTS
# ==================================================================
import arcpy
import csv
import os
from datetime import datetime
import warnings
import urllib3

# ==================================================================
# DISABLE SSL / SECURITY WARNING MESSAGES
# ==================================================================
warnings.filterwarnings("ignore", message="Unverified HTTPS request")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================================================================
# USER CONFIGURATION
# ==================================================================

# --- LOG OUTPUT LOCATION ---
LOG_OUTPUT_FOLDER = r"\\192.168.20.14\gis\Projects\2026_Projects\2026-05-Pipe-Raplcement-Dashboard\scripts\pipe-update-logs"   # CHANGE AS NEEDED

# --- ARCGIS ONLINE LOGIN ---
PORTAL_URL = "https://bedfordvagis.maps.arcgis.com"
AGOL_USERNAME = "brwa.sync_bedfordvagis"
AGOL_PASSWORD = "E&MBp^U@)4ybMWq"

# ==================================================================
# FEATURE SERVICE URL CONFIGURATION
# ==================================================================

# DESTINATION
COMBINED_PIPES_URL = (
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Combined_Pipes/FeatureServer/0"
)

# INPUTS2
FORCE_MAIN_SEWER_URL = (
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Force_Main_Sewer_2020/FeatureServer/0"
)

GRAVITY_MAIN_SEWER_URL = (
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Gravity_Main_Sewer_2020/FeatureServer/0"
)

WATER_MAIN_URL = (
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Waterline_BRWA_Version2021/FeatureServer/2"
)

# ==================================================================
# LOG FILE SETUP
# ==================================================================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"pipe-update_{timestamp}.csv"
log_path = os.path.join(LOG_OUTPUT_FOLDER, log_filename)

os.makedirs(LOG_OUTPUT_FOLDER, exist_ok=True)

log_file = open(log_path, mode="w", newline="", encoding="utf-8")
log_writer = csv.writer(log_file)
log_writer.writerow(["timestamp", "step", "tool", "status", "message"])

def log(step, tool, status, message=""):
    log_writer.writerow([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        step,
        tool,
        status,
        message
    ])
    log_file.flush()

# ==================================================================
# MAIN PROCESS
# ==================================================================
try:
    # --------------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------------
    log("Authentication", "SignInToPortal", "START")
    arcpy.SignInToPortal(PORTAL_URL, AGOL_USERNAME, AGOL_PASSWORD)
    log("Authentication", "SignInToPortal", "SUCCESS", f"Logged into {PORTAL_URL}")

    # --------------------------------------------------------------
    # FORCE MAIN SEWER
    # --------------------------------------------------------------
    log("Force Main Sewer", "Append", "START")
    arcpy.management.Append(
        inputs=FORCE_MAIN_SEWER_URL,
        target=COMBINED_PIPES_URL,
        schema_type="NO_TEST",
        field_mapping=r'SEMS_ID "SEMS ID" true true false 50 Text 0 0,First,#;Type "Type" true true false 50 Text 0 0,First,#',
        match_fields="GlobalID GlobalID",
        update_geometry="UPDATE_GEOMETRY",
        enforce_domains="NO_ENFORCE_DOMAINS",
        feature_service_mode="USE_FEATURE_SERVICE_MODE"
    )
    log("Force Main Sewer", "Append", "SUCCESS")

    arcpy.management.CalculateField(
        in_table=COMBINED_PIPES_URL,
        field="Type",
        expression="set_text(!Type!)",
        expression_type="PYTHON3",
        code_block="""def set_text(value):
    if value in (None, "", " "):
        return "Force Main Sewer"
    return value"""
    )
    log("Force Main Sewer", "CalculateField", "SUCCESS")

    # --------------------------------------------------------------
    # GRAVITY MAIN SEWER
    # --------------------------------------------------------------
    log("Gravity Main Sewer", "Append", "START")
    arcpy.management.Append(
        inputs=GRAVITY_MAIN_SEWER_URL,
        target=COMBINED_PIPES_URL,
        schema_type="NO_TEST",
        field_mapping=r'SEMS_ID "SEMS ID" true true false 50 Text 0 0,First,#;Type "Type" true true false 50 Text 0 0,First,#',
        match_fields="GlobalID GlobalID",
        update_geometry="UPDATE_GEOMETRY",
        enforce_domains="NO_ENFORCE_DOMAINS",
        feature_service_mode="USE_FEATURE_SERVICE_MODE"
    )
    log("Gravity Main Sewer", "Append", "SUCCESS")

    arcpy.management.CalculateField(
        in_table=COMBINED_PIPES_URL,
        field="Type",
        expression="set_text(!Type!)",
        expression_type="PYTHON3",
        code_block="""def set_text(value):
    if value in (None, "", " "):
        return "Gravity Main Sewer"
    return value"""
    )
    log("Gravity Main Sewer", "CalculateField", "SUCCESS")

    # --------------------------------------------------------------
    # WATER MAIN
    # --------------------------------------------------------------
    log("Water Main", "Append", "START")
    arcpy.management.Append(
        inputs=WATER_MAIN_URL,
        target=COMBINED_PIPES_URL,
        schema_type="NO_TEST",
        field_mapping=r'SEMS_ID "SEMS ID" true true false 50 Text 0 0,First,#;Type "Type" true true false 50 Text 0 0,First,#',
        match_fields="GlobalID GlobalID",
        update_geometry="UPDATE_GEOMETRY",
        enforce_domains="NO_ENFORCE_DOMAINS",
        feature_service_mode="USE_FEATURE_SERVICE_MODE"
    )
    log("Water Main", "Append", "SUCCESS")

    arcpy.management.CalculateField(
        in_table=COMBINED_PIPES_URL,
        field="Type",
        expression="set_text(!Type!)",
        expression_type="PYTHON3",
        code_block="""def set_text(value):
    if value in (None, "", " "):
        return "Water Main"
    return value"""
    )
    log("Water Main", "CalculateField", "SUCCESS")

except Exception as e:
    log("SCRIPT", "Execution", "ERROR", str(e))
    raise

finally:
    log("SCRIPT", "Execution", "SUCCESS", "Script completed")
    log_file.close()