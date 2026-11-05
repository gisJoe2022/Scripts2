

import arcpy
import logging
import os
from datetime import datetime
from arcgis.gis import GIS

# orange/force - ed4e33, Green Gravity - 6ef032, blue/water - 1d8ccc

# ============================================================
# CONFIGURATION
# ============================================================

# Saved ArcGIS Online Profile
AGOL_PROFILE = "brwa.sync"

# Hosted Feature Layer URLs
FORCE_MAINS_URL = (
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Force_Main_Sewer_2020/FeatureServer/0"
)
GRAVITY_MAINS_URL = (
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Gravity_Main_Sewer_2020/FeatureServer/0"
)
WATER_LINES_URL = (
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Waterline_BRWA_Version2021/FeatureServer/2"
)

# Target Dataset
COMBINED_PIPES = (
    r"\\nu\gis\Projects\2026_Projects\2026-07-Pipe-Raplcement-Dashboard\2026-05-Pipe-Raplcement-Dashboard.gdb\Combined_Pipes_fc"
)
# Log Folder
LOG_FOLDER = r"\\nu\gis\Projects\2026_Projects\2026-07-Pipe-Raplcement-Dashboard\scripts\logs"

# Backup File Geodatabase
BACKUP_GDB = r"\\nu\gis\Projects\2026_Projects\2026-07-Pipe-Raplcement-Dashboard\backups\pipes_backups.gdb"

# ============================================================
# LOGGING SETUP
# ============================================================

os.makedirs(LOG_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_FOLDER,
    f"COMBINED_PIPES_{datetime.now():%Y-%m-%d_%H-%M-%S}.log"
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger()

logger.info("================================================")
logger.info("Combined Pipes Update Started")
logger.info("================================================")

# ============================================================
# FUNCTIONS
# ============================================================

def get_count(dataset):
    """Return row count for a dataset."""
    try:
        return int(arcpy.management.GetCount(dataset)[0])
    except Exception:
        return -1

# ============================================================
# MAIN PROCESS
# ============================================================

try:

    # --------------------------------------------------------
    # Connect to ArcGIS Online
    # --------------------------------------------------------

    logger.info("Connecting to ArcGIS Online...")

    gis = GIS(profile=AGOL_PROFILE)

    logger.info(
        f"Connected as: {gis.users.me.username}"
    )

    # --------------------------------------------------------
    # Validate Source Layers
    # --------------------------------------------------------

    logger.info("Checking source layer counts...")

    force_count = get_count(FORCE_MAINS_URL)
    gravity_count = get_count(GRAVITY_MAINS_URL)
    water_count = get_count(WATER_LINES_URL)

    logger.info(f"Force Main Count: {force_count}")
    logger.info(f"Gravity Main Count: {gravity_count}")
    logger.info(f"Water Line Count: {water_count}")

    total_source_count = (
        force_count +
        gravity_count +
        water_count
    )

    logger.info(
        f"Total Source Records: {total_source_count}"
    )

    # Safety Check
    if total_source_count <= 0:
        raise Exception(
            "All source layers returned zero records. Process aborted."
        )

    # --------------------------------------------------------
    # Target Count Before Processing
    # --------------------------------------------------------

    target_before = get_count(COMBINED_PIPES)

    logger.info(
        f"Target Count Before Delete: {target_before}"
    )

    # --------------------------------------------------------
    # Backup Existing Combined Pipes
    # --------------------------------------------------------

    logger.info("Starting backup process...")

    try:

        # Verify backup geodatabase exists
        if not arcpy.Exists(BACKUP_GDB):
            raise Exception(
                f"Backup geodatabase does not exist: {BACKUP_GDB}"
            )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_fc_name = (
            f"Combined_Pipes_{timestamp}"
        )

        backup_fc = os.path.join(
            BACKUP_GDB,
            backup_fc_name
        )

        logger.info(
            f"Creating backup: {backup_fc}"
        )

        arcpy.management.CopyFeatures(
            COMBINED_PIPES,
            backup_fc
        )

        # Verify backup was created
        if not arcpy.Exists(backup_fc):
            raise Exception(
                "Backup feature class was not created."
            )

        source_count = get_count(COMBINED_PIPES)
        backup_count = get_count(backup_fc)

        logger.info(
            f"Source count: {source_count}"
        )

        logger.info(
            f"Backup count: {backup_count}"
        )

        # Verify record counts match
        if source_count != backup_count:
            raise Exception(
                "Backup validation failed. "
                f"Source count ({source_count}) "
                f"does not match backup count ({backup_count})."
            )

        logger.info(
            "Backup validation passed."
        )

    except Exception as ex:

        logger.error(
            f"BACKUP FAILED: {str(ex)}"
        )

        raise Exception(
            "Backup creation failed. "
            "Process aborted before deleting records."
        )

    # --------------------------------------------------------
    # Delete Existing Records
    # --------------------------------------------------------

    logger.info("Deleting existing records...")

    arcpy.management.DeleteRows(
        COMBINED_PIPES
    )

    logger.info("Delete completed.")

    # --------------------------------------------------------
    # Append Data
    # --------------------------------------------------------

    logger.info("Appending source layers...")

    arcpy.management.Append(
        inputs=[
            FORCE_MAINS_URL,
            GRAVITY_MAINS_URL,
            WATER_LINES_URL
        ],
        target=COMBINED_PIPES,
        schema_type="NO_TEST",

        # INSERT YOUR FIELD MAPPING STRING HERE
        field_mapping=r'SEMS_ID "SEMS ID" true true false 50 Text 0 0,First,#,Force_Main_Sewer,SEMS_ID,0,49,Gravity Main Sewer,SEMS_ID,0,49,Waterline_BRWA_Version 2021,SEMS_ID,0,49;Type "Type" true true false 50 Text 0 0,First,#;Material "Material" true true false 50 Text 0 0,First,#,Force_Main_Sewer,Material,0,49,Gravity Main Sewer,Material,0,49,Waterline_BRWA_Version 2021,Material,0,49;service_area "service_area" true true false 120 Text 0 0,First,#,Gravity Main Sewer,Service_Area,0,49,Waterline_BRWA_Version 2021,Service_Area,0,49,Force_Main_Sewer,ServiceArea,0,99;ServiceAreaGen "ServiceAreaGen" true true false 512 Text 0 0,First,#;estimatedOCI "Estimated OCI" true true false 8 Double 0 0,First,#,Force_Main_Sewer,estimatedOCI,-1,-1,Gravity Main Sewer,estimatedOCI,-1,-1,Waterline_BRWA_Version 2021,estimatedOCI,-1,-1;oci_class "OCI Class" true true false 2 Short 0 0,First,#;ActivityCost "Activity Cost" true true false 8 Double 0 0,First,#;Diamter "Diameter" true true false 8 Double 0 0,First,#,Force_Main_Sewer,Diameter,-1,-1,Gravity Main Sewer,Diameter,-1,-1,Waterline_BRWA_Version 2021,Diameter,-1,-1;Installed_Date "Installed Date" true true false 8 DateOnly 0 0,First,#,Force_Main_Sewer,Installed_Date,-1,-1,Gravity Main Sewer,Installed_Date,-1,-1,Waterline_BRWA_Version 2021,Installed_Date,-1,-1;GlobalID "GlobalID" false false true 38 GlobalID 0 0,First,#;created_user "created_user" true true true 255 Text 0 0,First,#,Force_Main_Sewer,created_user,0,254,Gravity Main Sewer,created_user,0,254,Waterline_BRWA_Version 2021,created_user,0,254;created_date "created_date" true true true 8 Date 0 1,First,#,Force_Main_Sewer,created_date,-1,-1,Gravity Main Sewer,created_date,-1,-1,Waterline_BRWA_Version 2021,created_date,-1,-1;last_edited_user "last_edited_user" true true true 255 Text 0 0,First,#,Force_Main_Sewer,last_edited_user,0,254,Gravity Main Sewer,last_edited_user,0,254,Waterline_BRWA_Version 2021,last_edited_user,0,254;last_edited_date "last_edited_date" true true true 8 Date 0 1,First,#,Force_Main_Sewer,last_edited_date,-1,-1,Gravity Main Sewer,last_edited_date,-1,-1,Waterline_BRWA_Version 2021,last_edited_date,-1,-1;Water_Type "Water_Type" true true false 255 Text 0 0,First,#,https:\\services3.arcgis.com\DXCmCcRcEQ793kMP\arcgis\rest\services\Waterline_BRWA_Version2021\FeatureServer\2,Water_Type,0,49',
        subtype="",
        feature_service_mode="USE_FEATURE_SERVICE_MODE",
        enforce_domains="NO_ENFORCE_DOMAINS",
        update_geometry="UPDATE_GEOMETRY"
    )

    target_after_append = get_count(COMBINED_PIPES)

    logger.info(
        f"Target Count After Append: {target_after_append}"
    )

    # --------------------------------------------------------
    # Calculate Type
    # --------------------------------------------------------

    logger.info("Calculating Type field...")

    type_exp = """
var id = $feature.SEMS_ID;

if (Left(id, 2) == "GM") {
    return "Gravity Main";
}
else if (Left(id, 2) == "FM") {
    return "Force Main";
}
else if (Left(id, 2) == "WL") {
    return "Water Line";
}
else {
    return $feature.Type;
}
"""

    arcpy.management.CalculateField(
        in_table=COMBINED_PIPES,
        field="Type",
        expression=type_exp,
        expression_type="ARCADE",
        field_type="TEXT"
    )

    logger.info("Type field calculation completed.")

# --------------------------------------------------------
    # Calculate Service Area Gen
    # --------------------------------------------------------

    logger.info("Calculating Service Area Gen field...")

    service_area_exp = """
var sa = $feature.Service_Area;
//var ty = Year(Now());

if (sa == "Central"){
    "Central"
    }
    else if (sa == "Central Water Distribution"){
          "Central"
    }
    else if (Find("Forest", sa)> -1){
      "Forest"
    }
    else if (Find("Cedar", sa)> -1){
      "Cedar Rock"
    }
     else if (Find("Montvale", sa)> -1){
      "Montvale"
    }
     else if (Find("Mountain", sa)> -1){
      "Mt. View Shores"
    }
    else if (Find("Paradise Point", sa)> -1){
      "Paradise Point"
    }
    else if (Find("SML Central", sa)> -1){
      "SML"
    }
    else if (Find("Stewartsville", sa)> -1){
      "Stewartsville"
    }
    else if (Find("Valley Mills", sa)> -1){
      "Valley Mills"
    }
    else if (Find("Central Sewer", sa)> -1){
    "Central"
    }
    else if (Find("Mariners Landing", sa)> -1){
      "Mariners Landing"
    }
    else if (Find("Moneta", sa)> -1){
      "Moneta"
    }
     else if (Find("Montvale", sa)> -1){
      "Montvale"
    }
    else {
      'Other'
    }
"""

    arcpy.management.CalculateField(
        in_table=COMBINED_PIPES,
        field="ServiceAreaGen",
        expression=service_area_exp,
        expression_type="ARCADE",
        field_type="TEXT"
    )

    logger.info("Service Area Gen field calculation completed.")

# --------------------------------------------------------
    # Calculate OCI Class
    # --------------------------------------------------------

    logger.info("Calculating OCI Class field...")

    ociclass_exp= """
var oci = $feature.estimatedOCI;

if (oci <10){
    1
    }
    else if (oci >= 10 && oci < 20){
      2
    }
    else if (oci >= 20 && oci < 30){
      3
    }
    else if (oci >= 30 && oci < 40){
      4
    }
     else if (oci >= 40 && oci < 50){
      5
    }
     else if (oci >= 50 && oci < 60){
      6
    }
     else if (oci >= 60 && oci < 70){
      7
    }
     else if (oci >= 70 && oci < 80){
      8
    }
     else if (oci >= 80 && oci < 90){
      9
    }
    else {
      10
    }
"""

    arcpy.management.CalculateField(
        in_table=COMBINED_PIPES,
        field="oci_class",
        expression=ociclass_exp,
        expression_type="ARCADE",
        field_type="TEXT"
    )


# --------------------------------------------------------
    # Calculate Activity Cost
    # --------------------------------------------------------

    logger.info("Calculating Activity Cost field...")

    activity_cost_exp= """
var type = $feature.Type
var len = $feature.Shape_Length

if (type == "Gravity Main"){
    (len*300)/1000
}
else {
  (len*160)/1000
}
"""

    arcpy.management.CalculateField(
        in_table=COMBINED_PIPES,
        field="ActivityCost",
        expression=activity_cost_exp,
        expression_type="ARCADE",
        field_type="TEXT"
    )

    logger.info("Activity Cost field calculation completed.")

# --------------------------------------------------------
    # Calculate Uknown Diameter
    # --------------------------------------------------------

    logger.info("Calculating Unknown Diameter field...")

    unknown_diameter_exp = """
var diam = $feature.Diamter

if (IsEmpty(diam))
  0
  else {
    diam
  }
"""

    arcpy.management.CalculateField(
        in_table=COMBINED_PIPES,
        field="Diamter",
        expression=unknown_diameter_exp,
        expression_type="ARCADE",
        field_type="TEXT"
    )

    logger.info("Unknown Diameter field calculation completed.")

    # --------------------------------------------------------
    # Final Validation
    # --------------------------------------------------------

    final_count = get_count(COMBINED_PIPES)

    logger.info(
        f"Final Target Count: {final_count}"
    )

    if final_count <= 0:
        raise Exception(
            "Validation failed. Target dataset contains zero records."
        )

    logger.info("Validation Passed")
    logger.info("Script completed successfully.")

except Exception as ex:

    logger.error("SCRIPT FAILED")
    logger.error(str(ex))

    try:
        logger.error(arcpy.GetMessages())
    except Exception:
        pass

    raise

finally:

    logger.info("Combined Pipes Update Finished")
    logger.info("================================================")