
//Add attribute information from a layer to another layers map pop-up.

var intersectLayer =Intersects(FeatureSetByName($map,"Elementary School Attendance Boundary"), $feature)

for (var f in intersectLayer){
return f.NAME