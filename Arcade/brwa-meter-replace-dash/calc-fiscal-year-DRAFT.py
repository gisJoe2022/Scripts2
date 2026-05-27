

## pyton version of above Arcade code for reference:
# logs into arcgis online


## NOT W0RKING
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import datetime
import pytz

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
AGOL_URL = "https://bedfordvagis.maps.arcgis.com"
USERNAME = "brwa.sync_bedfordvagis"
PASSWORD = "E&MBp^U@)4ybMWq"
ITEM_ID = "b962ffe1427043e29953dfe5e0d258bb"

FY_FIELD = "warranty_rep_yr"  
DATE_FIELD = "FY_code_test"  # "repFiscalYear"

# --------------------------------------------------
# LOG IN
# --------------------------------------------------
gis = GIS(AGOL_URL, USERNAME, PASSWORD)
print(f"Logged in as: {gis.users.me.username}")

# --------------------------------------------------
# GET FEATURE LAYER
# --------------------------------------------------
item = gis.content.get(ITEM_ID)

# If it's a Feature Layer Collection, grab layer 0
if hasattr(item, "layers") and len(item.layers) > 0:
    layer = item.layers[0]
else:
    layer = FeatureLayer(item.url)

print(f"Using layer: {layer.properties.name}")

# --------------------------------------------------
# QUERY FEATURES
# --------------------------------------------------
features = layer.query(
    where=f"{DATE_FIELD} IS NOT NULL",
    out_fields=f"{DATE_FIELD},{FY_FIELD}",
    return_geometry=False
).features

print(f"Processing {len(features)} features...")

# --------------------------------------------------
# FISCAL YEAR FUNCTION (July 1 start)
# --------------------------------------------------
from typing import Optional, Union

def fiscal_year_label(date_value: Optional[Union[int, float, datetime.datetime]]) -> Optional[str]:
    """
    Returns string like 'FY 35/36'
    Fiscal year starts July 1
    """
    if not date_value:
        return None

        utc_dt = datetime.datetime.fromtimestamp(date_value / 1000, tz=datetime.timezone.utc)
        local_tz = pytz.timezone("US/Eastern")
        d = utc_dt.astimezone(local_tz)
    if isinstance(date_value, (int, float)):
        d = datetime.datetime.fromtimestamp(date_value / 1000, tz=datetime.timezone.utc)
    elif isinstance(date_value, datetime.datetime):
        d = date_value
    else:
        return None

    year = d.year
    month = d.month  # Python months are 1–12

    # Flip FY on July 1
    if month >= 7:
        fy_end = year + 1
    else:
        fy_end = year
    return f"FY {fy_start % 100:02d}/{fy_end % 100:02d}"
    fy_start = fy_end - 1

    return f"FY {str(fy_start)[-2:]}/{str(fy_end)[-2:]}"

# --------------------------------------------------
# UPDATE FEATURES
# --------------------------------------------------
updates = []

for f in features:
    date_val = f.attributes.get(DATE_FIELD)
    fy = fiscal_year_label(date_val)

    if fy:
        f.attributes[FY_FIELD] = fy
        updates.append(f)

# --------------------------------------------------
# APPLY UPDATES
# --------------------------------------------------
if updates:
    result = layer.edit_features(updates=updates)
    # Check for errors in the result
    if "updateResults" in result:
        failed = [r for r in result["updateResults"] if not r.get("success", False)]
        if failed:
            print(f"Updated {len(updates) - len(failed)} records, {len(failed)} failed to update.")
            print("Failed updates:", failed)
        else:
            print(f"Updated {len(updates)} records successfully.")
    else:
        print("No updateResults found in response:", result)
else:
    print("No updates applied.")
