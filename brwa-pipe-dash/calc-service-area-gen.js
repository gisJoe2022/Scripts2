
// BRWA Pipe Dashboard Service Area Arcade Expression
// This Arcade expression is used in the BRWA Pipe Dashboard to determine the service area of a pipe segment. 
// It checks the value of the ServiceArea field and returns a simplified name for each service area. 
// If the service area does not match any of the specified values, it will return null.
// Joe Hayes: 5/4/2026

var sa = $feature.ServiceArea;
//var ty = Year(Now());

if (sa == "Central Sewer"){
    "Central"
    }
    else if (sa == "Forest Sewer"){
      "Forest"
    }
    else if (sa == "Mariners Landing Sewer"){
      "Mariners Landing"
    }
    else if (sa == "Moneta Sewer"){
      "Moneta"
    }
     else if (sa == "Montvale Sewer"){
      "Montvale"
    }




    //water service area gen calculate
    
var sa = $feature.Service_Area;
//var ty = Year(Now());

if (sa == "Central Water Distribution"){
    "Central"
    }
    else if (sa == "Forest Water"){
      "Forest"
    }
    else if (sa == "Forest Water (Boonsboro)"){
      "Forest"
    }
     else if (sa == "Montvale Water"){
      "Montvale"
    }
     else if (sa == "Mountain View Shores Water"){
      "Mt. View Shores"
    }
    else if (sa == "Paradise Point Water"){
      "Paradise Point"
    }
    else if (sa == "SML Central Water Distribution"){
      "SML Central"
    }
    else if (sa == "Stewartsville Water"){
      "Stewartsville"
    }
    else if (sa == "Valley Mills Water"){
      "Valley Mills"
    }
    else {
      'Other'
    }
