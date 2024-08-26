// Inserts the TILE_NAME record the section layer into the 
// TILE_NAME field in the Dedication layer. 

var getSec = FeatureSetByName($datastore, "production.SURVEY.section", ["TILE_NAME"])
var getSecInt = Intersects(getSec, $feature)
var sec = First(getSecInt)

if (sec == null) return {"errorMessage": "Section Not Found"}

return sec.TILE_NAME

