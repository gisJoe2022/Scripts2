# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NAME: LUD_Update.py
# Description: Uses production.LAND.UGB_Combined to update Distribution.LAND.UGB_Combined, 
# Purpose: 
# Author:      Joe Hayes
# Updated:     12/8/2021
# Copyright:   (c) Joe Hayes 2021
# Licence:     <your licence>
# ---------------------------------------------------------------------------

# import system modules
import arcpy
import sys

# enironment/workspace settings
arcpy.env.overwriteOutput = False

# local varaibales
prodUGB = "Database Connections\\washsde_production_boundary.sde\\Production.BOUNDARY.ugb"
prodUGBc = "Database Connections\\washsde_production_boundary.sde\\Production.BOUNDARY.UGB_Combined"
distUGB = "Database Connections\\zWrite_washsde_distribution_boundary.sde\\distribution.BOUNDARY.UGB"
distUGBc = "Database Connections\zWrite_washsde_distribution_boundary.sde\distribution.BOUNDARY.UGB_Combined"

try:
    # Export of GP process ran on 12/8/20215
    
    print ("")
    print ("Begining Update of Distribution UGB and UGB_Combined FCs...")
    print ("")

    print ("Truncating Production UGB...")
    # Truncate Prod UGB
    arcpy.management.TruncateTable(distUGB)
    print (" Truncate Complete")
    print ("")

    # Append Prod UGB to Dist UGB
    arcpy.management.Append(prodUGB, distUGB, "NO_TEST")
    print ("Append Complete")
    print ("")

    # # Truncate Distibution UGB Combined
    print ("Truncating Distibution UGB Combined...")
    arcpy.TruncateTable_management(distUGBc)
    print ("Truncate Complete")
    print ("")

    # # Append Production UGB Combined to Distribution UGB Combined
    print ("Production UGB Combined to Distribution UGB Combined...")
    arcpy.management.Append(prodUGBc, distUGBc, "NO_TEST")
    print ("")
    print ("Process Complete")
    print ("Have a Nice Day")
    print ("")
   
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])

    arcpy.AddError(e.args[0])
