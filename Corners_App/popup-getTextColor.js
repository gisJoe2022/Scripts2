

var fyear = $feature.Final_Year;
var am = $feature.AltMon;
var thisyear = Year(Now());

if (am == 'WLST'){
    '#FFFFFF'
}
    else if (am == '4COR'){
        '#FFFFFF'
    }
    else if ((am == 'NCC') && (IsEmpty(fyear))){
        '#FFFFFF'
    }
    else if ((IsEmpty(am) && IsEmpty(fyear))){
        '#FFFFFF'
    }
    else if (am == 'OTHC'){
        '#FFFFFF'
    }
    else if (fyear >= thisyear -5){
        '#FFFFFF'
    }
    else if ((fyear <= thisyear -6) && (fyear >= thisyear -10)){
        '#FFFFFF'
    }
      else if ((fyear <= thisyear -11) && (fyear >= thisyear -20)){
        '#FFFFFF'
    }
       else if ((fyear <= thisyear -21) && (fyear >= thisyear -35)){
        '#FFFFFF'
    }
       else if ((fyear <= thisyear -36) && (fyear >= thisyear -250)){
        '#FFFFFF'
    }
else
   return '#FF0000'