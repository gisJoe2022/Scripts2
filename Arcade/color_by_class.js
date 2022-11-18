// arcade popup color selector by class
// this one used in the Corners app to color code the 
// popus background to match the point symbology
// must be inserted in place of the html RGB colors in popup

// joe hayes Sepetember 2022
// some new stuff

var thisyear = Year(Now()); // unused at the moment
var label = $feature["Final_Year"];
var Labeler = When(label > 2017,'rgb(0, 197, 255)', // 5 fo fewer years
label < 2018 && label > 2012, 'rgb(0, 132, 168)', // 6-10 years
label < 2013 && label > 2002, 'rgb(112, 168, 0)', // 11-20 years
label < 2003 && label > 1987, 'rgb(255, 173, 0)', // 21-35 years
label < 1988 && label > 1700, 'rgb(197, 0, 255)', // >35 years
label == 'No Data', 'rgb(255, 255, 255)', // 'No Data' comes from another expression
'rgb(12, 0, 0)'); // other
return Labeler

// no data expression
IIf (IsEmpty($feature.Stamping), 'No Data', Proper($feature.Stamping, 'firstword'));

// pupup html                             expression inserted here
<div style="padding: 5px; background-color: {expression/expr0};"><b style="">
<font color="#ffffff" face="Tahoma" size="3" style="">{projName_4}</font></b></div><p style="margin: 0in;"><br /></p>


