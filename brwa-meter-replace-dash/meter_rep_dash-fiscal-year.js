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



