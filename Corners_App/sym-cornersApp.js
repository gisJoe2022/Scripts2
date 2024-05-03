// arcade symbology code.
// this one used in the Corners app to color code the 
// the point class symbols by year.

// joe hayes January 2023


// layer symbology
var fyear = $feature.Final_Year;
var am = $feature.AltMon;
var thisyear = Year(Now());

if (am == 'WLST'){
    'Willamette Stone'}
    else if (am == '4COR'){
        '4 Corner Stone'
    }
    else if ((am == 'NCC') && (IsEmpty(fyear))){
        'Non-Controling Corner'
    }
    else if ((IsEmpty(am) && IsEmpty(fyear))){
        'No BT Entry'
    }
    else if (am == 'OTHC'){
        'Maintained By Adjacent County'
    }
    else if (fyear >= thisyear -5){
        '5 Years Or Less'
    }
    else if ((fyear <= thisyear -6) && (fyear >= thisyear -10)){
        '6-10 Years'
    }
      else if ((fyear <= thisyear -11) && (fyear >= thisyear -20)){
        '11-20 Years'
    }
       else if ((fyear <= thisyear -21) && (fyear >= thisyear -35)){
        '21-35 Years'
    }
       else if ((fyear <= thisyear -36) && (fyear >= thisyear -250)){
        '>35 Years'
    }
else
   return 'other'