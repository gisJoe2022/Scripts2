

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


//tax lot popup
Tax lot: {TLID}
Owner: {OWNERNAME}
Site Address: {SITEADDR}
Acres: {A_T_ACRES} 
Land Value: {LANDVAL}
Improvement Value: {BLDGVAL}
Total Value: {TOTALVAL}
Year Built: {YEARBUILT}  
Sale Date: {SALEDATE}
Sale Price: {SALEPRICE}

//tax map expression
var lotid = $feature.TLID
var fivedig = Left(lotid, 5)
var seventest = MID(lotid, 5, 2)
var sevendig = Left(lotid, 7)

if (sevetest == "OO"){
    return "http://mtbachelor.co.washington.or.us/images/survey/dev/TaxMapPDF/" + Left($feature.TLID, 5) + ".pdf"
}
else{
    return "http://mtbachelor.co.washington.or.us/images/survey/dev/TaxMapPDF/" + Left($feature.TLID, 7) + ".pdf"
}

//new one
var seven = "http://mtbachelor.co.washington.or.us/images/survey/dev/TaxMapPDF/" + Left($feature.TLID, 7) + ".pdf"
var five = "http://mtbachelor.co.washington.or.us/images/survey/dev/TaxMapPDF/" + Left($feature.TLID, 5) + ".pdf"
var lotid = $feature.TLID
var seventest = MID(lotid, 5, 2)

if (seventest == "OO"){
    return five
}
else{
    return seven
}

