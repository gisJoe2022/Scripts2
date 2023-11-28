// arcade popup color selector by class
// this one used in the Corners app to color code the 
// popus background to match the point symbology
// must be inserted in place of the html RGB colors in popup

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

// text color
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
       else if ((fyear <= thisyear -36) && (fyear >= thisyear -150)){
        '#FFFFFF'
    }
else
   return '#FF0000'

// background color
var fyear = $feature.Final_Year;
var am = $feature.AltMon;
var thisyear = Year(Now());

var fyear = $feature.Final_Year;
var am = $feature.AltMon;
var thisyear = Year(Now());

if (am == 'WLST'){
    '#FFDE3E'}
    else if (am == '4COR'){
        '#FC921F'
    }
    else if ((am == 'NCC') && (IsEmpty(fyear))){
        '#000000'
    }
    else if ((IsEmpty(am) && IsEmpty(fyear))){
        '#ED5151'
    }
    else if (am == 'OTHC'){
        '#858585'
    }
    else if (fyear >= thisyear -5){
        '#00C5FF'
    }
    else if ((fyear <= thisyear -6) && (fyear >= thisyear -10)){
        '#0070FF'
    }
      else if ((fyear <= thisyear -11) && (fyear >= thisyear -20)){
        '#38A800'
    }
       else if ((fyear <= thisyear -21) && (fyear >= thisyear -35)){
        '#C500FF'
    }
       else if ((fyear <= thisyear -36) && (fyear >= thisyear -250)){
        '#FFAA00'
    }
else
   return 'wrong'



// no data expression
IIf (IsEmpty($feature.Stamping), 'No Data', Proper($feature.Stamping, 'firstword'));

// pupup html           expression inserted here for background color
<div style="padding: 5px; background-color: {expression/expr7};">
<font color="{expression/expr6}" face="Verdana" size="3">{expression/expr8}</font><br />
</div><p style="margin: 0in;"><b>Corner ID</b>: {CORNER_ID}<br /><b>AltMon</b>: {expression/expr0}<br />
</p><b>Visit Year</b>: {expression/expr1}<br /><b>BT Year</b>: {expression/expr2}<br /><b>Final Year</b>: {expression/expr3}


