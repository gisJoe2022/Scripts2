import os, arcpy, sys
cmd_folder = "\\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import gbl
from modEmail_3_7 import Send
from datetime import datetime

#aprx = arcpy.mp.ArcGISProject(r'')
roads_ams = "\\\\pwebgisapp1\\GIS_Process_Scripts\\ConnectionFiles\\nutsde_roadsams_ASSETS.sde"
prod_boundary = "\\\\pwebgisapp1\\GIS_Process_Scripts\\ConnectionFiles\\nutsde_production_boundary.sde"
sr = "CW_ServiceRequests_Dashboard"

Title = "UGB Boundary Script"
Message = ""
Error = 0

EmailTo = gbl.MyEmailRyan

#ScrptTimer = trktime.stopwatch()

# returns a list with all new service requests that have a null (None) attribute
def get_new_service_requests(fc):
    new_requests = []
    fields = ['UGB','REQUESTID']
    with arcpy.da.SearchCursor(fc,fields) as sCur:
        for row in sCur:
            #if row[0] == 'North Plains':
            if row[0] is None:
                new_requests.append(row[1])
    return new_requests

# returns a list of UGB boundaries within the 
def get_ugb(fc):
    ugb_name = []
    fields = ['UGB_Name']
    with arcpy.da.SearchCursor(fc,fields) as sCur:
        for row in sCur:
            ugb_name.append(row[0])
    return ugb_name

# returns a subset of new requestIDs that are located within each ugb boundarys
def update_ugb(ugb,new_records):
    if arcpy.Exists('records_lyr'):
        arcpy.Delete_management('records_lyr')
    new_records_lyr = arcpy.management.MakeFeatureLayer(os.path.join(roads_ams,sr),'records_lyr',where_clause="REQUESTID IN {0}".format(new_records))
    #result = arcpy.management.GetCount(new_records_lyr)
    if  arcpy.Exists("memory/intersected_records_ugb"):
        arcpy.Delete_management("memory/intersected_records_ugb")
        print('deleted intersection layer')
    update_list = []
    ugb_sql = "UGB_Name = '{0}'".format(ugb)
    if arcpy.Exists("{0}_lyr"):
        arcpy.Delete_management("{0}_lyr")
        print('deleted {0}_lyr'.format(ugb))
    ugb_lyr = arcpy.management.MakeFeatureLayer(os.path.join(prod_boundary,"ugb"),'{0}_lyr'.format(ugb),"UGB_Name = '{0}'".format(ugb))
    ugb_new_records = arcpy.analysis.Intersect([[new_records_lyr],[ugb_lyr]],"memory/intersected_records_ugb")
    #ugb_result = arcpy.management.GetCount(ugb_new_records)
    with arcpy.da.SearchCursor(ugb_new_records,['UGB','REQUESTID']) as sCur:
        for row in sCur:
            #print(row[1])
            update_list.append(row[1])
    del new_records_lyr
    return update_list

# updates table with specific ugb name
def update_ugb_records(fc,ugb,sql):
    with arcpy.da.UpdateCursor(fc,['UGB','REQUESTID'],sql) as uCur:
        for row in uCur:
            row[0] = '{0}'.format(ugb)
            print('update row for {0} in {1}'.format(row[1],ugb))
            uCur.updateRow(row)

# updates rural/outside ugb data attribute values
def update_non_ugb_records(fc,sql):
    with arcpy.da.UpdateCursor(fc,['UGB','REQUESTID'],sql) as uCur:
        for row in uCur:
            if row[0] is None:
                row[0] = 'No UGB'
                print('updated non ugb row {0}'.format(row[1]))
            uCur.updateRow(row)


def select_ugb(fc):
    arcpy.management.MakeFeatureLayer(os.path.join(prod_boundary,sr))
    
def init():
    arcpy.env.overwriteOutput = True

def main():
    # # Change to MyEmailRyan for dev
    # EmailTo = gbl.MyEmailRyan
    # !!!!Change back to GroupEmail when moving to Prod!!!.
    #EmailTo = gbl.MyEmailRyan

    #ScrptTimer = trktime.stopwatch()

   
    sr_fc = os.path.join(roads_ams,sr)
    new_sr_list = get_new_service_requests(sr_fc)
    new_records = tuple((new_sr_list))
    ugb_list = get_ugb(os.path.join(prod_boundary,"ugb"))
    print(ugb_list)
    for ugb in ugb_list:
        if ugb == 'Regional':
            print('pass')
            continue
        if ugb != 'Regional':
            ugb_records = tuple(update_ugb(ugb,new_records))
            if any(map(lambda x: any(x),ugb_records)) == True:   
                ugb_records_where =  "FOLDER = 'Operations' And REQUESTID IN {0}".format(ugb_records)
                print(ugb_records)
                update_ugb_records(sr_fc,ugb,ugb_records_where)
            else:
                continue
    #update remaining nulls:
    new_records_sql = "FOLDER = 'Operations' And REQUESTID IN {0}".format(new_records)
    update_non_ugb_records(sr_fc,new_records_sql)
        


if __name__ == '__main__':
    main()