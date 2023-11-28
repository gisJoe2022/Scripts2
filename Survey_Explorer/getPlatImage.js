
// used in the Address layer of survey explorer
// returns the plat filename from an intersect
// and appends it to the url to create a link to the plat image

var getVal = FeatureSetByName($datastore, "Plat", ["Filename"])
var getValIntersect = Intersects(getVal, $feature)
var Val = First(getValIntersect)
//var image = Text(Val.Filename)

if (Val == null) return Text(0)

"https://mtbachelor.co.washington.or.us/images/survey/Plats/" + Text(Val.Filename)
