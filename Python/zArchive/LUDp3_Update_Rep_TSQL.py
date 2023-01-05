# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NAME: LUD_Update.py
# Description: Uses production.LAND.LUD to update Production.LAND.LUD.Dissolve, 
#              Distribution.LAND.LUD and Distribution.LAND.lud.Dissolve.
# Purpose: 
# Author:      Joe Hayes
# Created:     6/4/2021
# Copyright:   (c) Joe Hayes 2021
# Licence:     <your licence>
# ---------------------------------------------------------------------------

# import system modules
import arcpy
import sys

# enironment/workspace settings
arcpy.env.overwriteOutput = False
#arcpy.env.workspace = ""

# TSQL local varaibales
prodLUD = "Database Connections\\tsqlgis1_production_land.sde\\production.LAND.LUD_1"
prodLUDdis = "Database Connections\\tsqlgis1_production_land.sde\\Production.LAND.LUD_Dissolve_1"
LUD_Dissolve = "Database Connections\\tsqlgis1_production_land.sde\\Production.LAND.LUD_Dissolve_1"
distLUD = "Database Connections\\tsqlgis1_distribution_land.sde\\distribution.LAND.LUD_1"
distLUDdis = "Database Connections\\tsqlgis1_distribution_land.sde\\distribution.LAND.lud_Dissolve"

prodLand = "Database Connections\\tsqlgis1_production_land.sde"
distLand = "Database Connections\\tsqlgis1_distribution_land.sde"
Replica = "LUDrep"

try:
    # Export of GP process ran on 4/9/2021
    # Synchronize Changes from prodLUD to disLUD

    # conflict_policy -- Not applicable for one way replicas, there is not conflict detection.
    # conflict_detection -- Not applicable for one way replicas, there is not conflict detection.
    # reconcile -- Only applicable for Checkout replicas
    
    print ("")
    print ("Begining to update Distribution LUD and LUD_Dissolve FCs...")
    print ("")
    print ("Syncronyzing prod.lud to dist.lud")
    arcpy.management.SynchronizeChanges("prodLand", "LUDrep", "distLand", "FROM_GEODATABASE1_TO_2", "IN_FAVOR_OF_GDB1", "BY_OBJECT", "")
    #arcpy.management.SynchronizeChanges(r"C:\Users\josephh\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\washsde_production_land.sde", "LUDrep", r"C:\Users\josephh\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\zWrite_washsde_distribution_land.sde", "FROM_GEODATABASE1_TO_2", "IN_FAVOR_OF_GDB1", "BY_OBJECT", "RECONCILE ")
    print ("Syncronyzation Complete")

    print ("")

    print ("")
    print ("Begining to update Distribution LUD and LUD_Dissolve FCs...")
    print ("")
    print ("Syncronyzing prod.lud to dist.lud")
    arcpy.management.SynchronizeChanges(geodatabase_1=prodLand, in_replica="LUDrep", 
        geodatabase_2=distLand, in_direction="FROM_GEODATABASE1_TO_2", conflict_policy="IN_FAVOR_OF_GDB1", 
        conflict_definition="BY_OBJECT", reconcile="RECONCILE ")
    print ("Syncronyzation Complete")
    print ("")

    # Delete PLD (production lud dissolve)
    print ("Deleting Production LUD Dissolve...")
    arcpy.Delete_management(prodLUDdis, "FeatureClass")
    print ("Complete")
    print ("")

    # # Dissolve New PLD (production lud dissolve)
    print ("Creating New Production LUD Dissolve...")
    arcpy.Dissolve_management(prodLUD, LUD_Dissolve, "LUD", "", "SINGLE_PART", "DISSOLVE_LINES")
    print ("Complete")
    print ("")

    # # Integrate New PLD (production lud dissolve)
    print ("Cleaning-up The New Production LUD Dissolve...")
    arcpy.Integrate_management(prodLUDdis, "1 Feet")
    print ("Complete")
    print ("")

    # # Truncate DL (distribution lud)
    print ("Truncating Distibution LUD...")
    arcpy.TruncateTable_management(distLUD)
    print ("Complete")
    print ("")

    # # Append PL (production lud) 2 DL (distribution lud)
    print ("Appending Production LUD to Distribution LUD...")
    arcpy.Append_management("'Database Connections\\washsde_production_land.sde\\production.LAND.LUD'", distLUD, "NO_TEST", "LUD \"Plan\" true true false 10 Text 0 0 ,First,#,Database Connections\\washsde_production_land.sde\\production.LAND.LUD,LUD,-1,-1;PlanDoc \"Comprehensive Plan Document\" true true false 50 Text 0 0 ,First,#,Database Connections\\washsde_production_land.sde\\production.LAND.LUD,PlanDoc,-1,-1;TLNO \"TLNO\" true true false 12 Text 0 0 ,First,#,Database Connections\\washsde_production_land.sde\\production.LAND.LUD,TLNO,-1,-1;GlobalID \"GlobalID\" false false false 38 GlobalID 0 0 ,First,#,Database Connections\\washsde_production_land.sde\\production.LAND.LUD,GlobalID,-1,-1;CP_No \"CP_No\" true true false 2 Short 0 5 ,First,#,Database Connections\\washsde_production_land.sde\\production.LAND.LUD,CP_No,-1,-1;Shape.area \"Shape.area\" false false true 0 Double 0 0 ,First,#;Shape.len \"Shape.len\" false false true 0 Double 0 0 ,First,#", "")
    print ("Complete")
    print ("")
 
    # # Truncate DLD (distribution lud dissolve)
    print ("Truncating Distribution LUD Dissolve...")
    arcpy.TruncateTable_management(distLUDdis)
    print ("Complete")
    print ("")

    # # Append PLD to DLD
    print ("Appending Production LUD Dissolve to Distribution LUD Dissolve...")
    arcpy.Append_management("'Database Connections\\washsde_production_land.sde\\production.LAND.LUD_Dissolve'", distLUDdis, "NO_TEST", "LUD \"Plan\" true true false 10 Text 0 0 ,First,#,Database Connections\\washsde_production_land.sde\\production.LAND.LUD_Dissolve,LUD,-1,-1;Shape.STArea() \"Shape.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\washsde_production_land.sde\\production.LAND.LUD_Dissolve,Shape.STArea(),-1,-1;Shape.STLength() \"Shape.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\washsde_production_land.sde\\production.LAND.LUD_Dissolve,Shape.STLength(),-1,-1", "")
    print ("Complete")
    print ("")
    print ("LUD Updates Complete")
    print ("")
    print ("Live Long And Prosper")
    print ("")
   
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])

      #arcpy.AddError(e.args[0])