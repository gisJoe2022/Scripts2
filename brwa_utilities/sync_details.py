

#
# code is not working - needs to be fixed
#


import requests
import datetime

# --- CONFIG ---
username = "brwa.sync_bedfordvagis"
password = "E&MBp^U@)4ybMWq"
service_url = "https://bedfordvagis.maps.arcgis.com/home/item.html?id=51bf387eb5a74afa84ef2b11d8424b95&sublayer=0"

# --- STEP 1: Generate Token ---
token_url = "https://www.arcgis.com/sharing/rest/generateToken"
token_params = {
    'f': 'json',
    'username': username,
    'password': password,
    'referer': 'https://www.arcgis.com',  # Required for AGOL
    'expiration': 60  # Token valid for 60 minutes
}

token_response = requests.post(token_url, data=token_params).json()
if 'token' not in token_response:
    raise Exception(f"Failed to generate token: {token_response}")
token = token_response['token']

# --- STEP 2: Get All Replicas ---
replicas_url = f"{service_url}/replicas"
params = {'f': 'json', 'token': token}
replicas_response = requests.get(replicas_url, params=params).json()

if 'replicas' in replicas_response:
    for replica in replicas_response['replicas']:
        print("\n--- Replica Summary ---")
        print(f"Name: {replica.get('replicaName')}")
        print(f"Owner: {replica.get('replicaOwner')}")
        print(f"Status: {replica.get('status')}")
        print(f"Sync Model: {replica.get('syncModel')}")
        print(f"Created: {datetime.datetime.fromtimestamp(replica.get('creationDate')/1000)}")
        print(f"Last Sync: {datetime.datetime.fromtimestamp(replica.get('lastSyncDate')/1000)}")

        # --- STEP 3: Get Full Details ---
        detail_url = f"{replicas_url}/{replica['replicaID']}"
        detail_response = requests.get(detail_url, params=params).json()
        print("\n--- Full Details ---")
        print(detail_response)  # Includes layers, sync direction, geometry changes, etc.
else:
    print("No replicas found or service is not sync-enabled.")