

//coners app - corner search

// layer symbology
// creates classes by calculating from current year
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
       else if ((fyear <= thisyear -36) && (fyear >= thisyear -150)){
        '>35 Years'
    }
else
   return 'wrong'





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

// corners with prior bt popup
<div style="padding: 5px; background-color: rgb(255, 255, 255); border: solid black; ">

<font color="#000000" face="Verdana" size="3">
<b>Corner With Prior BT</b></font></div><p style="margin: 0in;"><b>Corner ID</b>: {CORNER_ID}<br /><b>Notes</b>: {note}<br /></p>