var getVal = FeatureSetByName($datastore, "Production.TRANSPOR.TSP_LaneNumbers", ["Lanes"])
var getValIntersect = Intersects(getVal, $feature)
var Val = First(getValIntersect)

if (Val == null) return Text(0)

return Text(Val.Lanes)