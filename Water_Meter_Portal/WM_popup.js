
// Color Block Popup Header
<div style="padding: 5px; background-color: #0a8269;"><b style="">
<font color="#ffffff" face="Tahoma" size="3" style="">{projName_4}</font></b></div><p style="margin: 0in;"><br /></p>


//install date no data
IIf (IsEmpty($feature.Install_Date), 'No Data', Proper($feature.Install_Date));

//customer type nodata
IIf (IsEmpty($feature.Customer_Type), 'No Data', Proper($feature.Customer_Type));

//address nodata
IIf (IsEmpty($feature.Full_Address), 'No Address Data', Proper($feature.Full_Address));

// background color
var fyear = $feature.RepYear;
//var am = $feature.AltMon;
//var thisyear = Year(Now());

if (fyear == '2032'){
    '#a900e6'}
    else if ((fyear == 2031)){
        '#df73ff'
    }
    else if ((fyear == 2030)){
        '#1a53ff'
    }
    else if ((fyear == 2029)){
        '#00c5ff'
    }
    else if ((fyear == 2028)){
        '#38a800'
    }
    else if ((fyear == 2027)){
        '#4ce600'
    }
    else if ((fyear == 2026)){
        '#a87000'
    }
    else if ((fyear == 2025)){
        '#ffaa00'
    }
else
   return '#FFC0CB'