

import arcpy
import csv
import os

# AGOL login
arcpy.SignInToPortal('https://www.arcgis.com', 'your_username', 'your_password')

# Define the path to your feature class
feature_class = r'<path_to_your_feature_class>'

# List to store the ObjectIDs of features with true curves
curve_features_oids = []

# Create a search cursor to iterate over the features
with arcpy.da.SearchCursor(feature_class, ['OID@', 'SHAPE@']) as cursor:
    for row in cursor:
        # The hasCurves property returns True if the feature contains true curves
        if row[1].hasCurves:
            curve_features_oids.append(row[0])

# Print the ObjectIDs of the features that have true curves
print(f"Features with true curves (ObjectIDs): {curve_features_oids}")

# Write results to CSV
csv_path = r'<your_desired_csv_path>'
os.makedirs(os.path.dirname(csv_path), exist_ok=True)
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ObjectID'])
    for oid in curve_features_oids:
        writer.writerow([oid])
