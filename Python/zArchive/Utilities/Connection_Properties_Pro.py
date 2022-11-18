import arcpy, pprint
p = arcpy.mp.ArcGISProject('current')
m = p.listMaps()[0]
l = m.listLayers()[0]
pprint.pprint(l.connectionProperties)