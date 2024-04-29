# This code will iterate through all the maps in the Pro project 
# and save each layer to a layer file in the specified output folder. 
# The layer files will be named after the layer names.


import arcpy
import arcpy.management

# Set the input Pro project file
input_project = r"\\emcgis\nas\GISDATA\Workgroups\GISWebTeam\APRXs\LUT_ETS\Survey_Services\Survey_Services.aprx"

# Set the output folder location
output_folder = r"\\pfilepsb\SURVEY\SHARED\Data\GIS_Layers"

# Get all the maps in the Pro project
mxd = arcpy.mp.ArcGISProject(input_project)
#arcpy.mapp
maps = mxd.listMaps()

# Iterate through the maps and save each layer to a layer file
for map in maps:
    layers = map.listLayers()
    for layer in layers:
        output_layer = output_folder + "\\" + layer.name + ".lyrx"

        # Check if the output layer file already exists
        if not arcpy.Exists(output_layer):
            arcpy.management.SaveToLayerFile(layer, output_layer)
            print(output_layer)

# Save and close the Pro project
mxd.saveACopy(input_project)
mxd.close()