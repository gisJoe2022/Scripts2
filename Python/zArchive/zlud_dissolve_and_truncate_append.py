# arcpy
# ---------------------------------------------------------------------------
# lud_dissolve.py
# Created on: 2012-02-13 09:16:26.00000
# Nels Mickaelson
# Description: Creates a new feature layer for LUD (Land Use Districts)
# dissolves on field LUD and exports shapefile to APPGIS for use with legacy applications
#
# Updated 2016-06-23 by Brian Hanes
# Changed to drop creation of shapefile & add update of Distribution.LAND
# feature classes through the use of truncate/append
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Local variables:
Production_LAND_LUD = "Database Connections\\prod.Land.sde\\Production.LAND.LUD"
Production_LAND_LUD_Dissolve = "Database Connections\\prod.Land.sde\\Production.LAND.LUD_Dissolve"
Distribution_LAND_LUD = "Database Connections\\dist.Land.sde\\dist.LAND.LUD2"
Distribution_LAND_LUD_Dissolve = "Database Connections\\dist.Land.sde\\dist.LAND.LUD_Dissolve2"
# LUD_dissolve_shp = "\\\\emcgis\\nas\\gisdata\\Distro\\data\\shapefiles\\Washco\\land\\LUD_dissolve.shp"


# Process: Delete Dissolve Export
arcpy.Delete_management(Production_LAND_LUD_Dissolve, "FeatureClass")
arcpy.Dissolve_management(Production_LAND_LUD, Production_LAND_LUD_Dissolve, "LUD", "", "SINGLE_PART", "DISSOLVE_LINES")
# arcpy.Delete_management(LUD_dissolve_shp, "")
# arcpy.CopyFeatures_management(Production_LAND_LUD_Dissolve, LUD_dissolve_shp, "", "0", "0", "0")
arcpy.TruncateTable_management(Distribution_LAND_LUD)
arcpy.Append_management(Production_LAND_LUD, Distribution_LAND_LUD, "TEST")
arcpy.TruncateTable_management(Distribution_LAND_LUD_Dissolve)
arcpy.Append_management(Production_LAND_LUD_Dissolve, Distribution_LAND_LUD_Dissolve, "TEST")
