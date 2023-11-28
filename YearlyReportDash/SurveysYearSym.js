// distribution.survey.sv_suvey__app

// grabs the year from the filed date and 
// created symbology classes.

// Joe Hayes 
// 11/6/2023


// layer symbology
var filed = $feature.Filed;
var fy = Year(filed)
//var am = $feature.AltMon;
var thisyear = Year(Now());

if (fy == thisyear){
        return 'This Year'
    }
      else if (fy == thisyear -1){
        'Last Year'
    }
       else if (fy == thisyear -2){
        'Three Years Ago'
    }
       else if (fy == thisyear -3){
        'Fours Years Ago'
    }
else
   return 'Older'



//
var filed = $feature.Filed;
var fy = Year(filed)
//var am = $feature.AltMon;
var thisyear = Year(Now());

if (fy == thisyear){
        return 'This Year'
    }
      else if (fy == thisyear -1){
        'Last Year'
    }
       else if (fy == thisyear -2){
        'Three Years Ago'
    }
       else if (fy == thisyear -3){
        'Fours Years Ago'
    }
else
   return 'Older'


   
// layer symbology
var f = $feature.Filed;
//var fy = Year(filed)
//var thisyear = Year(Now());

if ((f >= '7-01-2023 00:00:00') && (f <= '6-30-2024 00:00:00')){
         'FY33/24'
}
    else if ((f >= Date(2022,07,01)) && (f <= Date(2023,06,30))){
           'Last Year'
}
else
   return 'other'


   // layer symbology
var f = $feature.Filed;
//var fy = Year(filed)
//var thisyear = Year(Now());

if ((f >= Date(2023,07,01)) && (f <= Date(2024,06,30))){
           'FY23/24'
}
    else if ((f >= Date(2022,07,01)) && (f <= Date(2023,06,30))){
           'FY22/23'
}
else
   return 'other'