// Adds the next sequencial ID for each Tile_Name (Section - polygon)
// in the Dedication layer (points).
// Developing this code for the section map updates.

var intpoly = FeatureSetByName($datastore, "Section")  // load polygon dataset
var pointvals = FeatureSetByName($datastore,"Dedication",['ID'],false)  // load point dataset

var polyname = ''
var polyvals = ''

for( var f in intpoly){    // loop through polys and see which one intersects
   if(Intersects($feature, f)){
       var polyname = f.TILE_NAME}  // set polyname variable to the TILE_NAME of intersecting polygon
}
if (!IsEmpty(polyname)){
    var polyvals = Filter(pointvals, `TILE_NAME = '${polyname}'`) // If not empty, filter points by intersecting poly name
}
var numarray = []
for (var n in polyvals){
    Push(numarray, n.ID)  // push all ID for points with TILE_NAME matching they polygon name
}

var newID = Max(numarray)+1 // get the max ID number and add 1 to it
if (IsEmpty(newID)){
    newID = 1
}
return {    // return a dictionary that updates TILE_NAME and ID in the points layer.
        "result": {
            "attributes": {
                //"TILE_NAME": polyname,
                "ID": Floor(newID, 0)
            },
        }
    }




