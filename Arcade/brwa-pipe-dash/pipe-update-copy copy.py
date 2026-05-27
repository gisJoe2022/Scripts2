

import arcpy
import os
import csv
from datetime import datetime
import urllib3

# --- SUPPRESS SSL WARNINGS (use only if needed) ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- ARCGIS ONLINE LOGIN ---
arcpy.SignInToPortal(
    "https://bedfordvagis.maps.arcgis.com",
    "brwa.sync_bedfordvagis",
    "E&MBp^U@)4ybMWq"
)
print("Signed in to:", arcpy.GetActivePortalURL())

# --- INPUTS ---
source_fc = r"\\192.168.20.14\gis\Projects\2026_Projects\2026-05-Pipe-Raplcement-Dashboard\2026-05-Pipe-Raplcement-Dashboard.gdb\Combined_Pipes_fc"
destination_gdb = r"\\192.168.20.14\gis\Projects\2026_Projects\2026-05-Pipe-Raplcement-Dashboard\Pipes_Combined_bu.gdb"
log_folder = r"\\192.168.20.14\gis\Projects\2026_Projects\2026-05-Pipe-Raplcement-Dashboard\logs"

append_sources = [
    r"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Waterline_BRWA_Version2021/FeatureServer/2", # Water Lines
    r"https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Force_Main_Sewer_2020/FeatureServer/0",  # Force Main Sewer
    r"https://services3.arcgis.com/DXCmCcRcEQ793kMP/ArcGIS/rest/services/Gravity_Main_Sewer_2020/FeatureServer/0"   # Gravity Main Sewer
]

# --- SETUP LOGGING ---
os.makedirs(log_folder, exist_ok=True)

log_file = os.path.join(
    log_folder,
    f"log_{datetime.now().strftime('%Y%m%d')}.csv"
)

def write_log(step, status, message):
    file_exists = os.path.isfile(log_file)

    with open(log_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Timestamp", "Step", "Status", "Message"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            step,
            status,
            message
        ])

# --- MAIN PROCESS ---
try:
    write_log("START", "INFO", "Script started")

    # =========================================================
    # STEP 1: EXPORT BACKUP WITH TIMESTAMP
    # =========================================================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fc_name = os.path.basename(source_fc)
    output_fc_name = f"{fc_name}_{timestamp}"
    output_fc = os.path.join(destination_gdb, output_fc_name)

    write_log("EXPORT", "INFO", f"Exporting to {output_fc}")

    arcpy.management.CopyFeatures(source_fc, output_fc)

    write_log("EXPORT", "SUCCESS", "Export completed")

    # =========================================================
    # STEP 2: TRUNCATE TARGET
    # =========================================================
    write_log("TRUNCATE", "INFO", f"Truncating {source_fc}")

    arcpy.management.TruncateTable(source_fc)

    write_log("TRUNCATE", "SUCCESS", "Truncate completed")

    # =========================================================
    # STEP 3: APPEND + CALCULATE TYPE FIELD
    # =========================================================
    write_log("APPEND", "INFO", "Starting append + Type population")

    """ # Ensure Type field exists
    existing_fields = [f.name for f in arcpy.ListFields(source_fc)]
    if "Type" not in existing_fields:
        arcpy.management.AddField(source_fc, "Type", "TEXT", field_length=50)
        write_log("SETUP", "INFO", "Added Type field") """

    # Define your sources
    source_configs = [
        {
            "url": append_sources[0],
            "name": "Water Lines",
            "type_value": "Water Line"
        },
        {
            "url": append_sources[1],
            "name": "Force Main Sewer",
            "type_value": "Force Main Sewer"
        },
        {
            "url": append_sources[2],
            "name": "Gravity Main Sewer",
            "type_value": "Gravity Main Sewer"
        }
    ]

    for cfg in source_configs:
        src = cfg["url"]
        name = cfg["name"]
        type_value = cfg["type_value"]

        try:
            write_log("APPEND", "INFO", f"Appending {name}")

            # --- Build field mappings ---
            field_mappings = arcpy.FieldMappings()

            def add_field_map(target_field, source_fc, source_field):
                fmap = arcpy.FieldMap()
                fmap.addInputField(source_fc, source_field)

                out_field = fmap.outputField
                out_field.name = target_field
                out_field.aliasName = target_field
                fmap.outputField = out_field

                field_mappings.addFieldMap(fmap)

            # --- DEFINE YOUR FIELD MAPS HERE ---
            # (Modify these to match your schemas)
            add_field_map("SEMS_ID", src, "SEMS_ID")
            add_field_map("Diameter", src, "Diameter")
            add_field_map("Material", src, "Material")
            add_field_map("Install_Date", src, "Install_Date")
            add_field_map("ServiceAreaGen", src, "ServiceAreaGen")
            add_field_map("estimatedOCI", src, "estimatedOCI")
            add_field_map("ActivityCost", src, "ActivityCost")
            add_field_map("oci_class", src, "oci_class")
            add_field_map("GlobalID", src, "GlobalID")
            

            # --- Count BEFORE append ---
            count_before = int(arcpy.management.GetCount(source_fc)[0])

            # --- Append ---
            arcpy.management.Append(
                inputs=src,
                target=source_fc,
                schema_type="NO_TEST",
                field_mapping=field_mappings
            )

            # --- Count AFTER append ---
            count_after = int(arcpy.management.GetCount(source_fc)[0])
            new_records = count_after - count_before

            write_log("APPEND", "SUCCESS", f"{name} appended ({new_records} records)")

            # --- Calculate Type field ---
            if new_records > 0:
                oid_field = arcpy.Describe(source_fc).OIDFieldName

                where_clause = f"{oid_field} > {count_before} AND Type IS NULL"

                write_log("CALCULATE", "INFO", f"Updating Type for {name}")

                # Create a temporary layer
                temp_layer = "temp_layer"

                arcpy.management.MakeFeatureLayer(source_fc, temp_layer)

                # Apply selection
                arcpy.management.SelectLayerByAttribute(
                    temp_layer,
                    "NEW_SELECTION",
                    where_clause
                )

                # Calculate only selected features
                arcpy.management.CalculateField(
                    temp_layer,
                    "Type",
                    f"'{type_value}'",
                    "PYTHON3"
                )

                # Clear selection (good practice)
                arcpy.management.SelectLayerByAttribute(temp_layer, "CLEAR_SELECTION")

                # Clean up
                arcpy.management.Delete(temp_layer)

                write_log("CALCULATE", "SUCCESS", f"{name} Type updated")

        except arcpy.ExecuteError:
            error_msg = arcpy.GetMessages(2)
            write_log("ERROR", "ARCPY", f"{name} - {error_msg}")

        except Exception as e:
            write_log("ERROR", "GENERAL", f"{name} - {str(e)}")

    write_log("APPEND", "INFO", "All append + Type updates completed")

    # =========================================================
    # STEP 5: REMOVE ATTACHMENTS
    # =========================================================
    write_log("ATTACHMENTS", "INFO", "Checking for attachments")

    desc = arcpy.Describe(source_fc)

    if hasattr(desc, "hasAttachments") and desc.hasAttachments:
        try:
            write_log("ATTACHMENTS", "INFO", "Removing attachments")

            arcpy.management.RemoveAttachments(source_fc)

            write_log("ATTACHMENTS", "SUCCESS", "Attachments removed")

        except arcpy.ExecuteError:
            error_msg = arcpy.GetMessages(2)
            write_log("ATTACHMENTS", "ERROR", error_msg)

        except Exception as e:
            write_log("ATTACHMENTS", "ERROR", str(e))
    else:
        write_log("ATTACHMENTS", "INFO", "No attachments found")

    # =========================================================
    # END
    # =========================================================
    write_log("END", "SUCCESS", "Script completed successfully")

except arcpy.ExecuteError:
    error_msg = arcpy.GetMessages(2)
    write_log("ERROR", "ARCPY", error_msg)
    print(error_msg)

except Exception as e:
    write_log("ERROR", "GENERAL", str(e))
    print(str(e))