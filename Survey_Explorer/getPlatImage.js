
// used in the Address layer of survey explorer
// returns the plat filename from an intersect
// and appends it to the url to create a link to the plat image

var getVal = FeatureSetByName($datastore, "Plat", ["Filename"])
var getValIntersect = Intersects(getVal, $feature)
var Val = First(getValIntersect)

if (Val == null) return "https://mtbachelor.co.washington.or.us/images/survey/NoImage.pdf" 

"https://mtbachelor.co.washington.or.us/images/survey/Plats/" + Text(Val.Filename)



// better var names
var getPlatImage = FeatureSetByName($datastore, "Plat", ["Filename"])
var getPlatImageIntersect = Intersects(getPlatImage, $feature)
var Val = First(getPlatImageIntersect)

if (Val == null) return "https://mtbachelor.co.washington.or.us/images/survey/NoImage.pdf" 

"https://mtbachelor.co.washington.or.us/images/survey/Plats/" + Text(Val.Filename)


// snipet
function compareAge(a,b){
    if (a['plat_list']<b['plat_list'])
      return -1;
    if (a['plat_list']>b['plat_list'])
      return 1;
    return 0;
  }
  return Text(compareAge);

  // ----------------------------------------


  var getData = FeatureSetByName($datastore, "Plat", ["Filename", "Recorded"])
var PlatDataInt = Intersects(getData, $feature)
//var Val = PlatDataInt


var platlist = ""
//var newarray = []

for (var k in PlatDataInt){
    platlist += k.Filename + TextFormatting.NewLine
}

return platlist

  var getData = FeatureSetByName($datastore, "Plat", ["Filename", "Recorded"])
var PlatDataInt = Intersects(getData, $feature)
//var Val = PlatDataInt



