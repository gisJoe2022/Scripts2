// Insert TILE_NAME
var getSec = FeatureSetByName($datastore, "Section", ["TILE_NAME"])
var getSecInt = Intersects(getSec, $feature)
var sec = First(getSecInt)

if (sec == null) return {"errorMessage": "Section Not Found"}

return sec.TILE_NAME

// Calculation Attribute Rule
// trigger: Insert
// field: ID

var seq = NextSequenceValue("SequenceName")
return seq

// Calculation Attribute Rule
// trigger: Insert
// field:ID

// Check if the current section meets your condition (e.g., based on some attribute)
var meetsCondition = $feature["TILE_NUM"] == "TILE_NUM" // Replace with your actual condition

// get the latest feature with a ID
var last_feature = First(OrderBy(Filter($featureset, "ID IS NOT NULL"), "OBJECTID DESC"))

// Get the last ID and add 1 if the condition is metvar 
seq = IIf(last_feature == null || !meetsCondition, 0, last_feature.ID + 1)

// get the last CW_ID and add 1
//var seq = IIf(last_feature == null, 0, last_feature.ID) + 1

return Number(seq)





// -------------------------------------------------------------------------------------

//curent good code

// Calculation Attribute Rule
// trigger: Insert
// field:ID

// get the latest feature with a ID
var last_feature = First(OrderBy(Filter($featureset, "ID IS NOT NULL"), "OBJECTID DESC"))
// get the last CW_ID and add 1
var seq = IIf(last_feature == null, 0, last_feature.ID) + 1

return Number(seq)




