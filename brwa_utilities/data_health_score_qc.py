
# ==========================================================
# IMPORTS
# ==========================================================

import arcpy
import pandas as pd
import os
import shutil
import smtplib
import traceback
import sys

from collections import Counter
from datetime import datetime, timedelta
from email.message import EmailMessage

# ==========================================================
# CONFIGURATION
# ==========================================================

# GDB CONNECTION
WGDB = r"\\SERVER\GIS\Water.sde"
SGDB = r"\\SERVER\GIS\Water.sde"

# FEATURE CLASSES
WATERMAIN_FC = os.path.join(WGDB, "Water.WaterMain")
VALVE_FC = os.path.join(WGDB, "Water.Valve")
HYDRANT_FC = os.path.join(WGDB, "Water.Hydrant")
SERVICE_FC = os.path.join(WGDB, "Water.ServiceLine")

# OUTPUT LOCATIONS
REPORT_FOLDER = r"\\SERVER\GIS\QCReports"
ARCHIVE_FOLDER = r"\\SERVER\GIS\QCReports\Archive"
LOG_FOLDER = r"\\SERVER\GIS\QCReports\Logs"

# EMAIL SETTINGS
SMTP_SERVER = "mail.company.org"
SMTP_PORT = 25
SENDER = "gis@company.org"
RECIPIENTS = [
    "joe.hayes@company.org"
]

DAYS_TO_KEEP = 90
INSPECTION_OVERDUE_DAYS = 365

# FIELD NAMES
ASSETID_FIELD = "ASSETID"
WM_DIAMETER_FIELD = "DIAMETER"
WM_MATERIAL_FIELD = "MATERIAL"
WM_INSTALLDATE_FIELD = "INSTALLDATE"

VALVE_SIZE_FIELD = "SIZE"
VALVE_TYPE_FIELD = "VALVETYPE"

HYD_LAST_INSPECTION_FIELD = "LASTINSPECTION"

# ==========================================================
# TIMESTAMPS
# ==========================================================

RUN_TIME = datetime.now()
STAMP = RUN_TIME.strftime("%Y%m%d_%H%M%S")

REPORT_FILE = os.path.join(
    REPORT_FOLDER,
    f"GIS_QC_Report_{STAMP}.xlsx"
)

LOG_FILE = os.path.join(
    LOG_FOLDER,
    f"GIS_QC_Log_{STAMP}.txt"
)

# ==========================================================
# CREATE FOLDERS
# ==========================================================

for folder in [
    REPORT_FOLDER,
    ARCHIVE_FOLDER,
    LOG_FOLDER
]:
    os.makedirs(folder, exist_ok=True)

# ==========================================================
# LOGGING
# ==========================================================

def log(message):

    msg = (
        f"{datetime.now():%Y-%m-%d %H:%M:%S}"
        f" | {message}"
    )

    print(msg)

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as logfile:

        logfile.write(msg + "\n")

# ==========================================================
# ARCHIVE OLD REPORTS
# ==========================================================

def archive_old_reports():

    cutoff = (
        datetime.now()
        - timedelta(days=DAYS_TO_KEEP)
    )

    for file in os.listdir(REPORT_FOLDER):

        if not file.endswith(".xlsx"):
            continue

        full_path = os.path.join(
            REPORT_FOLDER,
            file
        )

        modified = datetime.fromtimestamp(
            os.path.getmtime(full_path)
        )

        if modified < cutoff:

            shutil.move(
                full_path,
                os.path.join(
                    ARCHIVE_FOLDER,
                    file
                )
            )

# ==========================================================
# WATER MAIN QC
# ==========================================================

def run_watermain_qc():

    missing_assetid = []
    missing_material = []
    missing_installdate = []
    duplicate_ids = []

    asset_ids = []

    fields = [
        ASSETID_FIELD,
        WM_MATERIAL_FIELD,
        WM_INSTALLDATE_FIELD
    ]

    with arcpy.da.SearchCursor(
        WATERMAIN_FC,
        fields
    ) as cursor:

        for row in cursor:

            assetid = row[0]
            material = row[1]
            installdate = row[2]

            asset_ids.append(assetid)

            if assetid in [None, "", " "]:

                missing_assetid.append({
                    "AssetID": assetid
                })

            if material in [None, "", " "]:

                missing_material.append({
                    "AssetID": assetid
                })

            if installdate is None:

                missing_installdate.append({
                    "AssetID": assetid
                })

    counts = Counter(asset_ids)

    for assetid, count in counts.items():

        if assetid and count > 1:

            duplicate_ids.append({

                "AssetID": assetid,
                "DuplicateCount": count
            })

    return {

        "missing_assetid":
            missing_assetid,

        "missing_material":
            missing_material,

        "missing_installdate":
            missing_installdate,

        "duplicate_ids":
            duplicate_ids
    }

# ==========================================================
# WATER MAIN DIAMETER CHECK
# ==========================================================

def check_watermain_diameter():

    issues = []

    with arcpy.da.SearchCursor(
        WATERMAIN_FC,
        [
            ASSETID_FIELD,
            WM_DIAMETER_FIELD
        ]
    ) as cursor:

        for row in cursor:

            assetid = row[0]
            diameter = row[1]

            if diameter is None:

                issues.append({

                    "AssetID": assetid,
                    "Issue": "Missing Diameter"
                })

            elif diameter <= 0:

                issues.append({

                    "AssetID": assetid,
                    "Issue": "Invalid Diameter"
                })

    return issues

# ==========================================================
# VALVE CHECKS
# ==========================================================

def check_valves():

    size_issues = []
    type_issues = []

    with arcpy.da.SearchCursor(
        VALVE_FC,
        [
            ASSETID_FIELD,
            VALVE_SIZE_FIELD,
            VALVE_TYPE_FIELD
        ]
    ) as cursor:

        for row in cursor:

            assetid = row[0]

            if row[1] is None:

                size_issues.append({
                    "AssetID": assetid
                })

            if row[2] in [None, "", " "]:

                type_issues.append({
                    "AssetID": assetid
                })

    return size_issues, type_issues

# ==========================================================
# HYDRANT INSPECTION CHECKS
# ==========================================================

def check_hydrants():

    overdue = []

    cutoff = (
        datetime.now()
        - timedelta(
            days=INSPECTION_OVERDUE_DAYS
        )
    )

    with arcpy.da.SearchCursor(
        HYDRANT_FC,
        [
            ASSETID_FIELD,
            HYD_LAST_INSPECTION_FIELD
        ]
    ) as cursor:

        for row in cursor:

            assetid = row[0]
            inspect_date = row[1]

            if inspect_date is None:

                overdue.append({

                    "AssetID": assetid,
                    "Issue": "Missing Inspection"
                })

            elif inspect_date < cutoff:

                overdue.append({

                    "AssetID": assetid,
                    "LastInspection":
                        inspect_date
                })

    return overdue

# ==========================================================
# GEOMETRY CHECKS
# ==========================================================

def check_geometry(fc):

    output_table = os.path.join(
        "in_memory",
        f"geom_{os.path.basename(fc)}"
    )

    arcpy.management.CheckGeometry(
        fc,
        output_table
    )

    issues = []

    if int(arcpy.management.GetCount(
        output_table
    )[0]) > 0:

        with arcpy.da.SearchCursor(
            output_table,
            ["CLASS", "FEATURE_ID", "PROBLEM"]
        ) as cursor:

            for row in cursor:

                issues.append({

                    "Class": row[0],
                    "FeatureID": row[1],
                    "Problem": row[2]
                })

    return issues

# ==========================================================
# DOMAIN CHECKS
# ==========================================================

def check_domain_values():

    violations = []

    # CUSTOMIZE TO YOUR DOMAINS

    return violations

# ==========================================================
# SUBTYPE CHECKS
# ==========================================================

def check_subtypes(fc):

    issues = []

    desc = arcpy.Describe(fc)

    if not desc.subtypeFieldName:

        return issues

    valid_codes = list(
        arcpy.da.ListSubtypes(fc).keys()
    )

    with arcpy.da.SearchCursor(
        fc,
        [
            desc.subtypeFieldName,
            ASSETID_FIELD
        ]
    ) as cursor:

        for row in cursor:

            if row[0] not in valid_codes:

                issues.append({

                    "AssetID": row[1],
                    "Subtype": row[0]
                })

    return issues

# ==========================================================
# CREATE EXCEL REPORT
# ==========================================================

def create_report(results):

    with pd.ExcelWriter(
        REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        pd.DataFrame([{

            "Data Health Score":
                results["data_health_score"],

            "Total Assets":
                results["total_assets"],

            "Total Issues":
                results["total_issues"]

        }]).to_excel(

            writer,
            sheet_name="Executive Summary",
            index=False
        )

        for key, value in results.items():

            if isinstance(value, list):

                pd.DataFrame(value).to_excel(

                    writer,
                    sheet_name=key[:31],
                    index=False
                )

# ==========================================================
# HTML EMAIL
# ==========================================================

def send_email(results):

    html = f"""
    <html>
    <body>

    <h2>GIS Data Health Report</h2>

    <table border=1>

    <tr>
    <th>Metric</th>
    <th>Value</th>
    </tr>

    <tr>
    <td>Health Score</td>
    <td>{results['data_health_score']}%</td>
    </tr>

    <tr>
    <td>Total Issues</td>
    <td>{results['total_issues']}</td>
    </tr>

    </table>

    <p>See attached report.</p>

    </body>
    </html>
    """

    msg = EmailMessage()

    msg["Subject"] = (
        f"GIS QC Report {STAMP}"
    )

    msg["From"] = SENDER
    msg["To"] = ";".join(RECIPIENTS)

    msg.set_content(
        "HTML Email Attached"
    )

    msg.add_alternative(
        html,
        subtype="html"
    )

    with open(REPORT_FILE, "rb") as f:

        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=os.path.basename(REPORT_FILE)
        )

    with smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    ) as server:

        server.send_message(msg)

# ==========================================================
# MAIN
# ==========================================================

def main():

    archive_old_reports()

    wm = run_watermain_qc()

    wm_diam = check_watermain_diameter()

    valve_size, valve_type = (
        check_valves()
    )

    hydrant_overdue = (
        check_hydrants()
    )

    geometry_errors = []

    for fc in [
        WATERMAIN_FC,
        VALVE_FC,
        HYDRANT_FC,
        SERVICE_FC
    ]:
        geometry_errors.extend(
            check_geometry(fc)
        )

    domain_violations = (
        check_domain_values()
    )

    subtype_violations = []

    for fc in [
        WATERMAIN_FC,
        VALVE_FC,
        HYDRANT_FC,
        SERVICE_FC
    ]:
        subtype_violations.extend(
            check_subtypes(fc)
        )

    total_assets = 0

    for fc in [
        WATERMAIN_FC,
        VALVE_FC,
        HYDRANT_FC,
        SERVICE_FC
    ]:

        total_assets += int(
            arcpy.management.GetCount(fc)[0]
        )

    total_issues = (
        len(wm["missing_assetid"]) +
        len(wm["missing_material"]) +
        len(wm["missing_installdate"]) +
        len(wm["duplicate_ids"]) +
        len(wm_diam) +
        len(valve_size) +
        len(valve_type) +
        len(hydrant_overdue) +
        len(geometry_errors) +
        len(domain_violations) +
        len(subtype_violations)
    )

    health_score = round(
        (1 - (total_issues / max(total_assets,1))) * 100,
        2
    )

    results = {

        **wm,

        "wm_diameter_issues":
            wm_diam,

        "valve_size_issues":
            valve_size,

        "valve_type_issues":
            valve_type,

        "hydrant_overdue":
            hydrant_overdue,

        "geometry_errors":
            geometry_errors,

        "domain_violations":
            domain_violations,

        "subtype_violations":
            subtype_violations,

        "total_assets":
            total_assets,

        "total_issues":
            total_issues,

        "data_health_score":
            health_score
    }

    create_report(results)

    send_email(results)

# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    try:

        main()

        sys.exit(0)

    except Exception:

        log(traceback.format_exc())

        sys.exit(1)