
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

// ESRI Community Note
// 1. In a for loop with an array, your variable is the index. Use parentarray[index] to access the actual contents of that item.
// 2. You're adding the text string "$feature." to your fieldname variable, which you are then accessing with $feature.fieldname. 
//    Written out, that would be "$feature.$feature.", 
//    plus whatever your field name is.
// Accessing fields with dot notation only works with literal field names, and then only if the field name has no invalid characters.


