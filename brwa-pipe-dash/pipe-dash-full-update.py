

import arcpy
import logging
import os
from datetime import datetime
from arcgis.gis import GIS

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

# ============================================================
# LOGGING SETUP
# ============================================================

os.makedirs(LOG_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_FOLDER,
    f"CombinedPipes_{datetime.now():%Y-%m-%d_%H-%M-%S}.log"
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
    # Delete Existing Records
    # --------------------------------------------------------

    logger.info("Deleting existing records...")

    arcpy.management.DeleteRows(COMBINED_PIPES)

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
        field_mapping='SEMS_ID "SEMS ID" true true false 50 Text 0 0,First,#,Force_Main_Sewer,SEMS_ID,0,49,Gravity Main Sewer,SEMS_ID,0,49,Waterline_BRWA_Version 2021,SEMS_ID,0,49;Type "Type" true true false 50 Text 0 0,First,#;Diamter "Diameter" true true false 8 Double 0 0,First,#,Force_Main_Sewer,Diameter,-1,-1,Gravity Main Sewer,Diameter,-1,-1,Waterline_BRWA_Version 2021,Diameter,-1,-1;Material "Material" true true false 50 Text 0 0,First,#,Force_Main_Sewer,Material,0,49,Gravity Main Sewer,Material,0,49,Waterline_BRWA_Version 2021,Material,0,49;Install_Date "Install Date" true true false 8 Date 0 0,First,#,Force_Main_Sewer,Installed_Date,-1,-1,Gravity Main Sewer,Installed_Date,-1,-1,Waterline_BRWA_Version 2021,Installed_Date,-1,-1;ServicveAreaGen "Service Area Gen." true true false 120 Text 0 0,First,#,Force_Main_Sewer,ServiceAreaGen,0,119,Gravity Main Sewer,ServiceAreaGen,0,119,Waterline_BRWA_Version 2021,ServiceAreaGen,0,119;estimatedOCI "Estimated OCI" true true false 8 Double 0 0,First,#,Force_Main_Sewer,estimatedOCI,-1,-1,Gravity Main Sewer,estimatedOCI,-1,-1,Waterline_BRWA_Version 2021,estimatedOCI,-1,-1;ActivityCost "Activity Cost" true true false 8 Double 0 0,First,#,Force_Main_Sewer,ActivityCost,-1,-1,Gravity Main Sewer,ActivityCost,-1,-1,Waterline_BRWA_Version 2021,ActivityCost,-1,-1;oci_class "OCI Class" true true false 2 Short 0 0,First,#,Force_Main_Sewer,oci_class,-1,-1,Gravity Main Sewer,oci_class,-1,-1,Waterline_BRWA_Version 2021,oci_class,-1,-1;GlobalID "GlobalID" false false true 38 GlobalID 0 0,First,#,Force_Main_Sewer,GlobalID,-1,-1,Gravity Main Sewer,GlobalID,-1,-1,Waterline_BRWA_Version 2021,GlobalID,-1,-1;created_user "created_user" true true true 255 Text 0 0,First,#,Force_Main_Sewer,created_user,0,254,Gravity Main Sewer,created_user,0,254,Waterline_BRWA_Version 2021,created_user,0,254;created_date "created_date" true true true 8 Date 0 1,First,#,Force_Main_Sewer,created_date,-1,-1,Gravity Main Sewer,created_date,-1,-1,Waterline_BRWA_Version 2021,created_date,-1,-1;last_edited_user "last_edited_user" true true true 255 Text 0 0,First,#,Force_Main_Sewer,last_edited_date,-1,-1,Gravity Main Sewer,last_edited_date,-1,-1,Waterline_BRWA_Version 2021,last_edited_date,-1,-1;last_edited_date "last_edited_date" true true true 8 Date 0 0,First,#,Force_Main_Sewer,last_edited_user,0,254,Gravity Main Sewer,last_edited_user,0,254,Waterline_BRWA_Version 2021,last_edited_user,0,254;Installed_Date "Installed Date" true true false 8 DateOnly 0 0,First,#,Force_Main_Sewer,Installed_Date,-1,-1,Gravity Main Sewer,Installed_Date,-1,-1,Waterline_BRWA_Version 2021,Installed_Date,-1,-1',

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
    len*300
}
else {
  len*160
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