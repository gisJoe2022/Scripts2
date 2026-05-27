////////////////////////////////////////////////////////////////////
// desc: aracde code use in the meter dashboard for the director
// author: Joe Hayes
// updated: 1/27/2025
////////////////////////////////////////////////////////////////////



// Outputs fiscal year in format "FY 24/25" based on a date field
var d = $feature.warranty_rep_yr;

// Fiscal year ends the year AFTER July–December dates
// Month() in Arcade is 0-11 (July = 6)
var fyEndYear = Year(d) + IIf(Month(d) >= 6, 1, 0);
var fyStartYear = fyEndYear - 1;

// Last two digits of each year
var startYY = Right(Text(fyStartYear), 2);
var endYY = Right(Text(fyEndYear), 2);

if (IsEmpty(d) || isNaN(d) || d <= Date(2024, 6, 30)) {
    return "FY 00/24"
}
  else {
    return "FY " + startYY + "/" + endYY;
}











// calulate repacement year based on install date + 10 years
Number(Year($feature.Install_Date)) + 10


// Color Block Popup Header
<div style="padding: 5px; background-color: #2f85cc;"><b style="">
<font color="#ffffff" face="Tahoma" size="3" style="">{projName_4}</font></b></div><p style="margin: 0in;"><br /></p>


// Compare Install_Date and RepYear
// display the most recent year or 'No Data' if both are null
var indate = Year($feature.Install_Date)
var repyear = $feature.RepYear
// Check if both fields are null or NaN
if (IsEmpty(indate) || IsNan(indate)) {
  indate = null
}
if (IsEmpty(repyear) || IsNan(repyear)) {
  repyear = null
}
// Return "No Data" if both are null
if (IsEmpty(indate) && IsEmpty(repyear)) {
  return "No Data"
}
// Return the most recent year
if (IsEmpty(indate)) {
  return repyear
} else if (IsEmpty(repyear)) {
  return indate
} else {
  return Max(indate, repyear)
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Get unique values from the specified field
var uniqueValues = Distinct($feature.RepYear3);

// Define a function to classify based on the unique value
function classify(value) {
    return If(value == "Category1", "Class1", If(value == "Category2", "Class2", "Class3"));
}

// Iterate over each unique value and classify
var classifications = [];
ForEach(uniqueValues, function(value) {
    if ($feature.RepYear3 == value) {
        Push(classifications, classify(value));
    }
});

// Return the classifications array
return classifications;

///////////////////////////////////////////////////////////////////////////////////////////////////////////

// arcade symbology code.
// this one used in the Corners app to color code the 
// the point class symbols by year.

// joe hayes January 2023


// layer symbology
//var fyear = $feature.Final_Year;
var ry = $feature.RepYear3;
//var ty = Year(Now());

if (ry == 2032){
    '2032'
    }
    else if (ry == 2031){
      '2031'
    }
    else if (ry == 2030){
      '2030'
    }
    else if (ry == 2029){
      '2029'
    }
    else if (ry == 2028){
      '2027'
    }
    else if (ry == 2027){
      '2027'
    }
    else if (ry == 2026){
      '2026'
    }
    else if (ry == 2025){
      '2025'
    }
    else if (ry == 2024){
      '2024'
    }
else
   return 'other'