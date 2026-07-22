// BRWA Pipe Dashboard List Widget Arcade Expression
// This Arcade expression is used in the BRWA Pipe Dashboard to display pipe information in a color block format. 
// It combines the diameter and material of the pipe, and also includes the length of the pipe segment. 
// The expression also handles cases where the material is unknown or not specified.



var diam = $datapoint.Diameter;
var mat = $datapoint.Material;
var matAbbr = "";
var feet = Round($datapoint.Shape__Length, 1)
var oci = $datapoint.estimatedOCI
//var year = Year($datapoint.Install_Date);
//var thisyr = Year(Now());
//var age = thisyr - year


if (mat == 'CPVC'||mat == 'PVC'||mat == 'PVC C900'||mat == 'PVC SCH 40'||
           mat == 'PVC SDR 14'||mat == 'PVC SDR 17'||mat == 'PVC SDR 26'||
           mat == 'PVC SDR 35'||mat == 'PVC SDR 40'||mat == 'Yelomine') {
    matAbbr = 'PVC';
} else if (IsEmpty(mat))
    matAbbr = 'Unknown';
else {
    matAbbr = mat
}
var both = diam + '" ' + matAbbr;


return {
  textColor: '',
  backgroundColor: '',
  separatorColor:'',
  selectionColor: '',
  selectionTextColor: '',
   attributes: {
       attribute1: $datapoint.SEMS_ID,
       attribute2: both,
       attribute3: feet
   }
}