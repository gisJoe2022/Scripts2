import arcpy

#Environments
arcpy.env.workspace = r"\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\Transportation_Projects\2019\Reserves_BLI\Reserves_BLI_Julie.gdb"
arcpy.overwriteOutput = True

#set my varibales for this project
tazBLi = "Reserves_BLI_12012017_TAZ_2"

#Summarize the housing counts by TAZ
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "Reserves_BLI_12012017_TAZ_2"
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "Reserves_BLI_12012017_TAZ_2"
arcpy.Statistics_analysis(in_table="Reserves_BLI_12012017_TAZ_2", out_table="//Emcgis/nas/GISDATA/Workgroups/GISPlanning/Transportation_Projects/2019/Reserves_BLI/Reserves_BLI_Julie.gdb/Sum_Units_by_TAZ2", statistics_fields="UNITS SUM", case_field="TAZ_2162_2018_TAZ")
