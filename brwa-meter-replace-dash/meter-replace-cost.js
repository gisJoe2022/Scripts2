// BRWA Meter Replacement Dashboard
// Replace Cost by Diameter
// This Arcade expression calculates the replacement cost of a water meter based on its diameter.


var d = $feature.Diameter
var ind = $feature.installed_date

if (IsEmpty(d)){
  315
} else if (d == 5/8) {
  315
} else if (d == 3/4){
  566
} else if (d == 1){
  565
} else if (d == 1.5){
  995
} else if (d == 2){
  1361
} else if (d == 3){
  3900
} else if (d == 4){
  4800
} else if (d == 6){
  6800
} else if (d == 8){
  9000
} else if (d == 10){
  10900
}
