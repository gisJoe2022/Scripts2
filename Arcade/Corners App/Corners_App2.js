

//coners app - corner search
//altmon
IIf (IsEmpty($feature["AltMon"]), 'No Data', $feature["AltMon"]);

//visit year
IIf (IsEmpty($feature["Visit_Year"]), 'No Data', Text($feature["Visit_Year"], '####'));

//bt year
IIf (IsEmpty($feature["BT_Year"]), 'No Data', Text($feature["BT_Year"], '####'));

//final year
IIf (IsEmpty($feature["Final_Year"]), 'No Data', Text($feature["Final_Year"], '####'));

// corners - search color by year - {expression/expr4}
var thisyear = Year(Now()); // unused at the moment
var label = $feature["Final_Year"];
var Labeler = When(label > 2017,'rgb(0, 197, 255)', // 5 fo fewer years
label < 2018 && label > 2012, 'rgb(0, 132, 168)', // 6-10 years
label < 2013 && label > 2002, 'rgb(112, 168, 0)', // 11-20 years
label < 2003 && label > 1987, 'rgb(255, 173, 0)', // 21-35 years
label < 1988 && label > 1700, 'rgb(197, 0, 255)', // >35 years
label == 'No Data', 'rgb(255, 255, 255)', // No Data comes from another expression
'rgb(12, 0, 0)'); // other
return Labeler

//tax map expression
// main tax map 
// 12/20/2022

// evaluates TLID to pass correct string to url 
// to get the correct tax map.
var tlid = $feature.TLNO    // '3S1060000301'

var gn = MID(tlid, 0, 7)
var m1 = MID(tlid, 3, 2)
var m2 = MID(tlid, 5, 2)
var m3 = MID(tlid, 3, 4)
var m4 = MID(tlid, 5, 1)
var m5 = MID(tlid, 6, 1)


var l3 = Left(tlid, 3)
var l5 = Left(tlid, 5)
var l6 = Left(tlid, 6)

var p1 = "https://mtbachelor.co.washington.or.us/images/colortaxmaps/"
var p2 = ".pdf"

//tests for 3 char taxmaps
if (m1 == '00'){
    if (m3 == '0000') {
        gn = l3
    }
    if (m3 != '0000') {
        gn = l3 + m4
    }
}
// returns 5 char taxmap if above is false
else if (m2 == '00'){
    gn = l5
    //return p1 + l5 + p2
}
else if (m5 == '0'){
    gn = l6
    
}
return p1 + gn + p2
