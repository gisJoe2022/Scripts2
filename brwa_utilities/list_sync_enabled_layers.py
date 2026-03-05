


from arcgis.gis import GIS
import pandas as pd
import os
import getpass
import datetime
import sys
import logging
import urllib3

# Suppress HTTPS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration - adjust as needed or set via environment variables
PORTAL_URL = os.getenv("BRWA_PORTAL_URL", "https://bedfordvagis.maps.arcgis.com/")
USERNAME = os.getenv("BRWA_SYNC_USERNAME", "brwa.sync_bedfordvagis")
# Password is preferred from env var; fallback to interactive prompt
PASSWORD = os.getenv("BRWA_SYNC_PASSWORD") or getpass.getpass("Portal password: ")

SEARCH_QUERY = os.getenv("BRWA_SEARCH_QUERY", 'categories:"BRWA"')
MAX_ITEMS = int(os.getenv("BRWA_MAX_ITEMS", "1000"))
OUTPUT_FOLDER = os.getenv("BRWA_OUTPUT_FOLDER", r"S:\Projects\2025_Projects\202508_Layer_Cleanup")

# Basic console logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

def get_item_url(item):
    """Return the most useful URL for the item, if available."""
    url = getattr(item, "url", None)
    if url:
        return url
    # Try layers list
    try:
        layers = getattr(item, "layers", None)
        if layers:
            first = layers[0]
            # layer objects may have .url or be dict-like
            return getattr(first, "url", None) or (first.get("url") if isinstance(first, dict) else None)
    except Exception:
        pass
    return None


def is_item_sync_enabled(item):
    """Robustly determine if the item supports sync.

    We prefer explicit properties (syncEnabled/supportsSync) and also
    check the capabilities string as a fallback. Default is False.
    """
    props = getattr(item, "properties", None) or {}
    if isinstance(props, dict):
        if props.get("syncEnabled") is True:
            return True
        if props.get("supportsSync") is True:
            return True

    caps = getattr(item, "capabilities", "") or ""
    if isinstance(caps, str) and "Sync" in caps:
        return True

    # If layers are present, check layer-level properties as a last resort
    try:
        for lyr in getattr(item, "layers", []) or []:
            lyr_props = getattr(lyr, "properties", None) or (lyr if isinstance(lyr, dict) else {})
            if isinstance(lyr_props, dict) and (lyr_props.get("syncEnabled") or lyr_props.get("supportsSync")):
                return True
    except Exception:
        pass

    return False


def main():
    # Authenticate
    try:
        gis = GIS(PORTAL_URL, USERNAME, PASSWORD)
        logger.info("Signed in to portal %s as %s", PORTAL_URL, USERNAME)
    except Exception as e:
        logger.exception("Failed to sign in to portal: %s", e)
        return 1

    # Search
    try:
        items = gis.content.search(query=SEARCH_QUERY, item_type="Feature Layer", max_items=MAX_ITEMS)
        logger.info("Search returned %d items for query: %s", len(items), SEARCH_QUERY)
    except Exception as e:
        logger.exception("Search failed: %s", e)
        return 1

    sync_enabled_layers = []
    for item in items:
        try:
            if is_item_sync_enabled(item):
                sync_enabled_layers.append({
                    "Title": item.title,
                    "ID": item.id,
                    "Owner": item.owner,
                    "URL": get_item_url(item),
                    "Sync Enabled": True,
                })
        except Exception as e:
            # Log warning and continue
            logger.warning("Failed to evaluate item %s: %s", getattr(item, 'id', None), e)

    if not sync_enabled_layers:
        logger.info("No sync-enabled layers found with category 'BRWA'.")
        return 0

    # Prepare timestamped output paths
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    output_file = os.path.join(OUTPUT_FOLDER, f"sync_enabled_brwa_layers_{ts}.csv")
    log_file = os.path.join(OUTPUT_FOLDER, f"sync_enabled_brwa_layers_{ts}.log")

    # Ensure output folder exists
    try:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    except Exception as e:
        logger.exception("Could not create output folder '%s': %s", OUTPUT_FOLDER, e)
        return 1

    # Add file handler so logs are also written to a dated logfile in the output folder
    try:
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(message)s"))
        logger.addHandler(fh)
        logger.info("Logging to file: %s", log_file)
    except Exception as e:
        logger.warning("Could not create log file handler %s: %s", log_file, e)

    try:
        df = pd.DataFrame(sync_enabled_layers)
        df.to_csv(output_file, index=False)
        logger.info("CSV file saved at: %s", output_file)
    except Exception as e:
        logger.exception("Failed to write CSV: %s", e)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
