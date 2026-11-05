
// BRWA Pipe Dashboard Service Area Arcade Expression
// This Arcade expression is used in the BRWA Pipe Dashboard to determine the service area of a pipe segment. 
// It checks the value of the ServiceArea field and returns a simplified name for each service area. 
// If the service area does not match any of the specified values, it will return null.
// Joe Hayes: 5/4/2026


var sa = $feature.Service_Area;
//var ty = Year(Now());

if (Find("Central", sa)> -1){
    "Central"
    }
    else if (Find("Forest", sa)> -1){
      "Forest"
    }
    else if (Find("Cedar", sa)> -1){
      "Cedar Rock"
    }
     else if (Find("Montvale", sa)> -1){
      "Montvale"
    }
     else if (Find("Mountain", sa)> -1){
      "Mt. View Shores"
    }
    else if (Find("Paradise Point", sa)> -1){
      "Paradise Point"
    }
    else if (Find("SML Central", sa)> -1){
      "SML Central"
    }
    else if (Find("Stewartsville", sa)> -1){
      "Stewartsville"
    }
    else if (Find("Valley Mills", sa)> -1){
      "Valley Mills"
    }
    else if (Find("Central Sewer", sa)> -1){
    "Central"
    }
    else if (Find("Mariners Landing", sa)> -1){
      "Mariners Landing"
    }
    else if (Find("Moneta", sa)> -1){
      "Moneta"
    }
     else if (Find("Montvale", sa)> -1){
      "Montvale"
    }
    else {
      'Other'
    }
