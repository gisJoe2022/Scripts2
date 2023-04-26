# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# CPO_Update.py
# Created on: 2019-07-24 16:40:16.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import smtplib



# Local variables:
prodCPO = "Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO"
Updated_Disro_CPO = prodCPO
distroCPO = "Database Connections\\zWRITE.washsde.Distribution.Boundary.sde\\distribution.BOUNDARY.CPO"
Disto_w_deleted_table = distroCPO

server = smtplib.SMTP('smtp.gmail.com', 587)

# Outlook Server Name: 55a62efe-2c7d-4e70-9bbe-44a7625fbb61@co.washington.or.us
# Username: Joseph_Hayes@co.washington.or.us

# Process: Truncate Table
arcpy.TruncateTable_management(distroCPO)

# Process: Append
arcpy.Append_management("'Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO'", distroCPO, "NO_TEST", "distribution.BOUNDARY.CPO.AREA \"distribution.BOUNDARY.CPO.AREA\" true true false 8 Double 5 18 ,First,#;PERIMETER \"PERIMETER\" true true false 8 Double 5 18 ,First,#;CPO2001A_ \"CPO2001A_\" true true false 8 Double 0 11 ,First,#;CPO2001A_I \"CPO2001A_I\" true true false 8 Double 0 11 ,First,#;JUR \"JUR\" true true false 2 Short 0 5 ,First,#;NUM \"NUM\" true true false 2 Short 0 5 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,NUM,-1,-1;SIERRACD \"SIERRACD\" true true false 14 Text 0 0 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,SIERRACD,-1,-1;NAME \"NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,NAME,-1,-1;ADDRESS \"ADDRESS\" true true false 100 Text 0 0 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,ADDRESS,-1,-1;CITY \"CITY\" true true false 100 Text 0 0 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,CITY,-1,-1;STATE \"STATE\" true true false 16 Text 0 0 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,STATE,-1,-1;ZIP \"ZIP\" true true false 16 Text 0 0 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,ZIP,-1,-1;CPO_AREA \"CPO_AREA\" true true false 50 Text 0 0 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,CPO_AREA,-1,-1;URL \"URL\" true true false 250 Text 0 0 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,URL,-1,-1;community_name \"community_name\" true true false 250 Text 0 0 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,community_name,-1,-1;Shape.area \"Shape.area\" false false true 0 Double 0 0 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,Shape.area,-1,-1;Shape.len \"Shape.len\" false false true 0 Double 0 0 ,First,#,Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.CPO,Shape.len,-1,-1", "")




_________________________________________________________________________________
"""The first step is to create an SMTP object, each object is used for connection 
with one server."""

#import smtplib
#server = smtplib.SMTP('smtp.gmail.com', 587)

#Next, log in to the server
#server.login("youremailusername", "password")

#Send the mail
#msg = "
#Hello!" # The /n separates the message from the headers
#server.sendmail("you@gmail.com", "target@example.com", msg)