import os, arcpy

# globals
# database
#db = r'C:\Users\StevenC\Documents\Projects\street_transfer\street_transfer\street_transfer.gdb'
# sub database for testing
import tarfile

import future.backports.email.iterators
import future.backports.html.entities

db = r'C:\Users\StevenC\Documents\Projects\street_transfer\street_transfer\street_transfer_20220519_01.gdb'
# project
aprx = arcpy.mp.ArcGISProject(r'C:\Users\StevenC\Documents\Projects\street_transfer\street_transfer\street_transfer.aprx')
# input feature

def collect_features(aprx):
    for m in aprx.listMaps():
        if m.name == 'download':
            for lyr in m.listLayers():
                print(lyr.name)
                """if lyr.isBroken():
                    print('broken')"""
                if lyr.name in ['World Topographic Map', 'World Hillshade']:
                    print(" (BROKEN) " + lyr.name)
                if " " in lyr.name:
                    n = lyr.name
                    lyr_name = n.replace(" ","_")
                    arcpy.FeatureClassToFeatureClass_conversion(lyr, db, lyr_name,"1=1")
                else:
                    arcpy.FeatureClassToFeatureClass_conversion(lyr, db, lyr.name,"1=1")

def create_route(db):
    arcpy.env.workspace = db
    for fc in arcpy.ListFeatureClasses():
        if fc != 'washstr':
            continue
        if fc == 'washstr':
            # dissolve the centerline
            continue

def get_vertices(target_fc, db):

    """for fc in arcpy.ListFeatureClasses():
        print(fc)
        if fc != target_fc:
            continue
        if fc == 'non_identical_segments':
            with arcpy.da.SearchCursor(target_fc,'OBJECTID') as sCur:
                for row in sCur:
                    arcpy.SelectLayerByAttribute_management(fc_lyr,"NEW_SELECTION",sql)
                    arcpy.FeatureVerticesToPoints_management(fc_lyr, os.path.join(db, "{0}_endpoints".format(lyr.name,)), "BOTH_ENDS")
                    #arcpy.FeatureVerticesToPoints_management(fc, os.path.join(db, "{0}_midpoint".format(fc)), "MID")
        arcpy.MakeFeatureLayer_management(os.path.join(db,"non_identical_segments"))"""
    arcpy.env.workspace = db

    result = arcpy.GetCount_management(target_fc)
    print(result)
    count = int(result.getOutput(0))
    fc_lyr = arcpy.MakeFeatureLayer_management(target_fc)
    for i in range(int(count)):
        print(i)
        sql = "OBJECTID = {0}".format(i)
        print(sql)
        arcpy.SelectLayerByAttribute_management(fc_lyr, "NEW_SELECTION", sql)
        # ---- note: try exluding end points.  don't think they are needed -->
        #arcpy.management.FeatureVerticesToPoints(fc_lyr,os.path.join(db,'endpoint_{0}'.format(str(i))), "BOTH_ENDS")
        arcpy.management.FeatureVerticesToPoints(fc_lyr, os.path.join(db, "midpoint_{0}".format(str(i))), "MID")
        print('exported end points')

        arcpy.analysis.Buffer(fc_lyr,
                              os.path.join('buffer_{0}'.format(str(i))),
                              "70 Feet", "FULL", "ROUND", "NONE", None, "PLANAR")
        print('created buffer')

    for i in range(int(count)):
        wash_lyr = arcpy.MakeFeatureLayer_management(os.path.join(db,"WashStr"))
        arcpy.management.SelectLayerByLocation(wash_lyr, "WITHIN", os.path.join(db,'buffer_{0}'.format(i)), None, "NEW_SELECTION", "NOT_INVERT")

        if i == 0:
            arcpy.lr.CreateRoutes(wash_lyr, "FNAME", os.path.join(db, 'route_main'),
                                  "LENGTH", None, None, "UPPER_LEFT", 1, 0, "IGNORE", "INDEX")
            arcpy.lr.CreateRoutes(wash_lyr, "FNAME", os.path.join(db,'route_{0}'.format(i)),
                                  "LENGTH", None, None, "UPPER_LEFT", 1, 0, "IGNORE", "INDEX")
        if i > 0:
            arcpy.lr.CreateRoutes(wash_lyr, "FNAME", os.path.join(db, 'route_{0}'.format(i)),
                                  "LENGTH", None, None, "UPPER_LEFT", 1, 0, "IGNORE", "INDEX")



def get_transfer_dictionary(target_mid_point_fc, database):
    arcpy.env.workspace = database
    fields_list = []
    fields_dict = {}
    featureclasses = arcpy.ListFeatureClasses()
    for fc in featureclasses:
        if os.path.join(database, fc) != target_mid_point_fc:
            continue
        if os.path.join(database, fc) == target_mid_point_fc:
            fields = arcpy.ListFields(target_mid_point_fc)

            for f in fields:
                #print(f.name)
                """fields_list.append(field.name)
                fields_dict.update({field.name: {'type': field.type, 'length': field.length}})"""
                fn = f.name
                ft = f.type
                fp = f.precision
                fs = f.scale
                fl = f.length
                if fn == 'OBJECTID' or ft == 'Shape':
                    pass
                else:
                    fields_dict.update({f.name:{'type':f.type,'length':f.length}})
    return fields_dict

def get_transfer_fields(target_mid_point_fc, database):
    arcpy.env.workspace = database
    fields_list = []
    featureclasses = arcpy.ListFeatureClasses()
    for fc in featureclasses:
        if os.path.join(database, fc) != target_mid_point_fc:
            continue
        if os.path.join(database, fc) == target_mid_point_fc:
            fields = arcpy.ListFields(target_mid_point_fc)
            for f in fields:
                fn = f.name
                if fn == 'OBJECTID' or fn == 'Shape':
                    pass
                else:
                    fields_list.append(f.name)
    return fields_list

def create_boundary(target_fc, distance_ft, reference_fc, db):
    arcpy.env.workspace = db
    for fc in arcpy.ListFeatureClasses():
        if fc != target_fc:
            continue
        if fc == target_fc:
            arcpy.analysis.Buffer(target_fc, os.path.join(db,"{0}_Buffer".format(target_fc),
                                  "{0} Feet".format(distance_ft), "FULL", "ROUND", "ALL", None, "PLANAR"))
            arcpy.management.SelectLayerByLocation("TSP_FunctionalClass", "ARE_IDENTICAL_TO", "WashStr", None,
                                                   "NEW_SELECTION", "INVERT")

def compare_feature(target_fc,sql):
    print('-------new evaluation-------')
    """arcpy.management.SelectLayerByLocation(target_fc, "WITHIN_A_DISTANCE", reference_fc, "10 Feet",
                                           "NEW_SELECTION", "NOT_INVERT")"""
    #target_id =
    #
    compare_dict = {}
    #fields = ['OBJECTID', 'SHAPE@']
    fields = arcpy.ListFields(target_fc)
    fields_list = []
    fields_dict = {}
    for field in fields:
        fields_list.append(field.name)
        fields_dict.update({field.name: {'type': field.type, 'length': field.length}})
    for i in range(len(fields_list)):
        if fields_list[i] == 'Shape':
            fields_list[i] = 'SHAPE@'
    print(fields_list)
    print(fields_dict)
    print(sql)

    with arcpy.da.SearchCursor(target_fc, fields_list, sql) as sCur:
        for row in sCur:
            compare_dict.update({row[0]: {'shape': row[1]}})
            #print(compare_dict)
    return compare_dict[row[0]]['shape']

def get_transfer_evaluation(target_fc,reference_fc):
    d_list = ["mid", "mid_buffer", "non_identical_segments", "endpoint_*", "vertices_*", 'buffer_*']
    for d in d_list:
        if arcpy.Exists(os.path.join(db, d)):
            arcpy.Delete_management(os.path.join(db, d))
            print('deleted {0}'.format(d))
    transfer_list = []
    target_lyr = arcpy.MakeFeatureLayer_management(target_fc)
    reference_lyr = arcpy.MakeFeatureLayer_management(reference_fc)
    arcpy.management.SelectLayerByLocation(target_lyr, "ARE_IDENTICAL_TO", reference_lyr, None, "NEW_SELECTION", "INVERT")
    arcpy.FeatureClassToFeatureClass_conversion(target_lyr,db,'non_identical_segments')
    with arcpy.da.SearchCursor(target_lyr, ['OBJECTID']) as sCur:
        for row in sCur:
            transfer_list.append(row[0])

    arcpy.management.FeatureVerticesToPoints(target_lyr, os.path.join(db, "mid"), "MID")
    print('created midpoint')
    # below not needed - delete?
    #mid_buffer = arcpy.Buffer_analysis(target_lyr, os.path.join(db, "mid_buffer"), "10 FEET").getOutput(0)
    #print('created buffer')
    #select_wash_st = arcpy.SelectLayerByLocation_management(reference_lyr, "INTERSECT", mid_buffer, None, "NEW_SELECTION", "NOT_INVERT").getOutput(0)


    del target_lyr, reference_lyr
    return transfer_list

def get_target_midpoint(target_fc,reference_fc,sql):
    transfer_dict = {}
    target_lyr = arcpy.MakeFeatureLayer_management(target_fc).getOutput(0)
    reference_lyr = arcpy.MakeFeatureLayer_management(reference_fc).getOutput(0)
    arcpy.management.FeatureVerticesToPoints(target_lyr, os.path.join(db, "mid"),"MID")
    print('created midpoint')
    mid_buffer = arcpy.Buffer_analysis(os.path.join(db,"mid"), os.path.join(db, "mid_buffer"), "10 FEET")
    print('created buffer')

    arcpy.SelectLayerByLocation_management(reference_lyr, "INTERSECT", mid_buffer, None, "NEW_SELECTION", "NOT_INVERT")

def generate_segment_vertices(input_fc,reference_fc,db):

    #do something
    fields = ['OBJECTID']
    with arcpy.da.SearchCursor(input_fc, fields) as sCur:
        for row in sCur:
            segments = arcpy.MakeFeatureLayer_management(input_fc, "segment_lyr",
                                                         "OBJECTID = {0}".format(row[0])).getOutput(0)
            v_o = arcpy.management.FeatureVerticesToPoints(segments, os.path.join(db,"vertices_{0}".format(row[0])), "ALL").getOutput(0)

            arcpy.SelectLayerByLocation_management(v_o, "INTERSECT", reference_fc, None,
                                                   "NEW_SELECTION", "NOT_INVERT")
            print('intersect')
            arcpy.Delete_management(segments)


def evaluate_segment_fc(db):
    arcpy.env.workspace = db
    match_list = []
    mismatch_list = []
    featureclasses = arcpy.ListFeatureClasses('vertices*')
    for fc in featureclasses:
        print(fc)
        fc_lyr = arcpy.MakeFeatureLayer_management(fc)
        full_count = arcpy.GetCount_management(fc_lyr)
        print(full_count)
        arcpy.management.SelectLayerByLocation(fc_lyr, "INTERSECT", os.path.join(db,"WashStr"), None,
                                               "NEW_SELECTION", "NOT_INVERT").getOutput(0)
        selected_count = arcpy.GetCount_management(fc_lyr)
        if full_count == selected_count:
            match_list.append(fc)
        if full_count != selected_count:
            mismatch_list.append(fc)
    print(match_list)
    print(mismatch_list)

def load_main_route(db):
    arcpy.env.workspace = db

    def grab_route_data(fc,dictionary):
        fields = ['OBJECTID', 'SHAPE@', 'FNAME', 'Shape_length', 'UrbRur', 'F_Label', 'FClass2', 'created_user',
                  'created_date', 'last_edited_user', 'last_edited_date', 'GlobalID', 'ORIG_FID']
        with arcpy.da.SearchCursor(fc, fields) as sCur:
            for row in sCur:
                print(row)
                dictionary.update({row[11]: {'SHAPE': row[1], 'FNAME': row[2], 'Shape_length': row[3], 'UrbRur': row[4],
                                            'F_Label': row[5], 'FClass2': row[6], 'created_user': row[7],
                                            'created_date': row[8], 'last_edited_user': row[9],
                                            'last_edited_date': row[10], 'GlobalID': row[11], 'ORIG_FID': row[12]}})

    route_dict = {}
    featureclasses = arcpy.ListFeatureClasses('route_*')
    print(featureclasses)
    for fc in featureclasses:
        if fc == 'route_main':
            continue
        if fc.startswith('route'):
            grab_route_data(fc,route_dict)
    insert_fields = ['SHAPE@', 'FNAME', 'Shape_length', 'UrbRur', 'F_Label', 'FClass2', 'created_user',
              'created_date','last_edited_user', 'last_edited_date', 'GlobalID', 'ORIG_FID']

    target_fc = os.path.join(db, 'route_main')
    iCur = arcpy.da.InsertCursor(target_fc, insert_fields)
    for k,v in route_dict.items():
        print(k)
        print(v['SHAPE'],v['FNAME'])
        iCur.insertRow((v['SHAPE'], v['FNAME'], v['Shape_length'], v['UrbRur'], v['F_Label'],
                        v['FClass2'], v['created_user'], v['created_date']
                        ,v['last_edited_user'], v['last_edited_date']
                        ,v['GlobalID'], v['ORIG_FID']))
        #iCur.insertRow((v['SHAPE']))
        print('inserted row')


def init():
	arcpy.env.overwriteOutput = True

def main():
    init()
    #arcpy.env.overwriteOutput = True

    #collect_features(aprx)
    # create base data for target_fc
    # step one - get not intersecting line segments (ex. wash streets - and TSP functional class)

    evaluation_id_list = get_transfer_evaluation(os.path.join(db,"TSP_FunctionalClass"),os.path.join(db,"WashStr"))
    print(evaluation_id_list)

    sql = 'OBJECTID in {0}'.format(tuple(evaluation_id_list))
    print(sql)
    print(compare_feature(os.path.join(db, "TSP_FunctionalClass"), sql))
    compare_feature(os.path.join(db, "TSP_FunctionalClass"), sql)
    get_vertices(os.path.join(db, "TSP_FunctionalClass"), db)

    # -- create validation statement on creating "generate_segment_vertices"
    # -- global application on TSP Functional Class took considerable processing
    # generate_segment_vertices(os.path.join(db, "TSP_FunctionalClass"), os.path.join(db, "WashStr"), db)
    # -- evaluation of individual segments to generate comparison between vertices and WashSt
    # (eval - function) evaluate_segment_fc(db)
    #

    target_fc = os.path.join(db, "TSP_FunctionalClass")
    result = arcpy.GetCount_management(target_fc)
    print(result)
    count = int(result.getOutput(0))

    for i in range(count):
        if i > 0:
            continue
        else:
            #get_transfer_fields(os.path.join(db, "midpoint_{0}".format(i)),db)
            #print('added field to route_{0}'.format(i))
            add_fields = get_transfer_dictionary(os.path.join(db, "midpoint_{0}".format(i)), db)
            add_field_names = get_transfer_fields(os.path.join(db,"midpoint_{0}".format(i)), db)

    print(add_fields)

    for i in range(count):
        print('route_{0}'.format(i))
        for k, v in add_fields.items():
            if k == 'Shape':
                pass
            elif i == 0:
                arcpy.AddField_management(os.path.join(db, "route_main"), k, v['type'], v['length'])
                print('added field')
                arcpy.AddField_management(os.path.join(db, "route_{0}".format(i)), k, v['type'], v['length'])
                print('added field')
            elif i > 0:
                arcpy.AddField_management(os.path.join(db, "route_{0}".format(i)), k, v['type'], v['length'])
                print('added field')

    print(add_field_names)

    for i in range(count):
        target_feature = os.path.join(db, "midpoint_{0}".format(i))
        #target_feature = r"memory\"midpoint_{0}".format(i)"
        transfer_feature = os.path.join(db, "route_{0}".format(i))
        #transfer_feature = r"memory\"route_{0}".format(i)
        get_field_values = []
        with arcpy.da.SearchCursor(target_feature, add_field_names) as sCur:
            for row in sCur:
                for ii in range(len(add_field_names)):
                    get_field_values.append(row[ii])
                get_field_values.append(row)
        print(get_field_values)
        values_dict = dict(zip(add_field_names, get_field_values))
        print(values_dict)
        with arcpy.da.UpdateCursor(transfer_feature, add_field_names) as uCur:
            for row in uCur:
                for iii in range(len(values_dict)):
                    row[iii] = get_field_values[iii]
                uCur.updateRow(row)

    load_main_route(db)
    # notes
    # 1. Identify non identify features (export TSP)
    # 2. Iterate through TSP features and generate following output
    # 3. 1. create a buffer/select (50 feet) within a distance of each TSP
    # 4. export wash streets geometries.  Usually wash street geometries are ->
    # -- many to one examples of tsp func class.
    # -- dissolve wash streets into single 'route' feature.
    # -- collect schema & attribution from the tsp functional class for that segment -->
    # -- create temp/memory copy of dissolve route (could load all of this into dictionary)
    # 5. Iterate through individual features or dictionary and load segment routes into ->
    # -- feature.  This output would be correctly attributed functional class with washington -->
    # --- street geometry.
    # -- Evaluate QC.
    # -- 1. evaluate based on attribution (global/local ID) that data is correct.
    # -- 2. topology, generate gap analysis and identify and spatial gaps and Identify.
    # -- 3. if gaps exist (extract from wash street and merge with new feature to close gap).


    # --

if __name__ == '__main__':
    main()
    # get_target_midpoint(os.path.join(db, "TSP_FunctionalClass"), os.path.join(db, "WashStr"), sql)
    # get_vertices(os.path.join(db,"TSP_Bikeways"), db)
    # create_boundary(target_fc, 50, db)


