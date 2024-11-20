# ---------------------------------------------------------------------------
# gbl.py
# Created on: 2023-05-02 
#
# Description:  Global variables for Python Scripts
# ---------------------------------------------------------------------------

import os, sys

#cmd_folder = "\\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules\\"
cmd_folder = "\\pwebgisapp1.co.washington.or.us\GIS_Process_Scripts\LUT_Survey"

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class PassMessage():
    appendMessage = ""
    fail = 0
    elapsedTime = 0
    rtnText = ""

# Data Connections
#RoadsAMS
RoadsAMS_Assets = "\\\\pwebgisapp1\\GIS_Process_Scripts\\ConnectionFiles\\nutsde_roadsams_ASSETS.sde"
RoadsAMS_Assets_TSQL = "\\\\emcgis\\NAS\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\tsqlgisn1_RoadsAMS_Assets.sde"
#nutsdeProd
NpSTREETS = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreets.sde\\production.STREETS."
NpTRANSPOR = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpTranspor.sde\\production.TRANSPOR."
NpSTREETS = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreets.sde\\production.STREETS."
NpSTREETSQC = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC."
#nutsdeDistro
NdSTREETS = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NdStreets.sde\\distribution.STREETS."
NdSTREETS = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NdStreets.sde\\distribution.STREETS."
NdTRANSPOR = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NdTranspor.sde\\distribution.TRANSPOR."
#GISbug
WBUG_TRANSPOR="\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\WGISBUG.Transpor.sde\\gisbug.TRANSPOR."

#sql
RdNet = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\SQL1_RoadNet.sde\\RoadNet.dbo."
#other
MetroStr = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\Streets\\Transfers\\From_Metro\\str.gdb\\"
StrSave = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\Streets\\Transfers\\From_Metro\\"
dcNpSTREETSQC="\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\psqlgisn1_production_streets_qc.sde"

# Layers
#streets
streets = "str"
WashStr_2913 = "WashStr_2913_vw"
WashStr = "WashStr"
PMSAll_Roads = "PMSAll_Roads"
Ops_PMSAll_Roads = "Ops_PMSAll_Roads"
PMSAllRoads_Convert_WashStr = "PMSAllRoads_Convert_WashStr"
WC_Pavement = "WC_Pavement"
#linnear referencing
lrs_IRIS_Routes ="lrs_IRIS_Routes"
LRS_Routes ="LRS_Routes"
LID_Routes = "LID_Routes"
IntersectionUnique = "IntersectionUnique"
XsectID="XsectID"
intersections="intersections"
lrs_OutsideCounty = "lrs_OutsideCounty"
lrs_IRIS_allMP = "lrs_IRIS_allMP"
lrs_IRIS_allMP_lines = "lrs_IRIS_allMP_lines"
LRS_allMP = "LRS_allMP"
LRS_allMP_lines = "LRS_allMP_lines"

# Views
vw_PMS_All_Roads = "vw_PMS_All_Roads"
vw_IRIS_Mileposts = "vw_IRIS_Mileposts"
vw_IRIS_Milepost_Lines = "vw_IRIS_Milepost_Lines"
#other
URMD_Area_RoadsAMS = "URMD_Area"


# Email Groups
GroupEmail = "Steven_Cotterill@washingtoncountyor.gov, mike_holscher@washingtoncountyor.gov, brian_hanes@washingtoncountyor.gov, Richard_Crucchiola@washingtoncountyor.gov"
MyEmailRyan = "Steven_Cotterill@washingtoncountyor.gov"
