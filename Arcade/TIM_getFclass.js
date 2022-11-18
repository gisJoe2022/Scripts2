var getVal = FeatureSetByName($datastore, "Production.TRANSPOR.TSP_FunctionalClass", ["F_Label"])
var buf = Buffer($feature, 20, 'feet')
var getValIntersect = Intersects(getVal, $feature)
var Val = First(getValIntersect)

if (Val == null) return "Local"

return Val.F_Label