// Arcade expression to generate a label for waterline diameter and merial types
// This expression generates a label that combines the diameter and material type of a waterline feature.
// The material type is abbreviated based on predefined conditions.
// author: joe hayes
// date: 2025-06-11

var diam = $feature.Diameter;
var mat = $feature.Material;
var matAbbr = "";

if (mat == 'Aquamine') {
    matAbbr = 'AQU';
} else if (mat == 'Asbestos Cement') {
    matAbbr = 'AC';
} else if (mat == 'Brass') {
    matAbbr = 'BR';
} else if (mat == 'Cast Iron') {
    matAbbr = 'CI';
} else if (mat == 'Clay') {
    matAbbr = 'TC';
} else if (mat == 'Concrete') {
    matAbbr = 'CON';
} else if (mat == 'Copper') {
    matAbbr = 'CPR';
} else if (mat == 'Galvanized Steel') {
    matAbbr = 'GVL';
} else if (mat == 'CPVC'||mat == 'PVC'||mat == 'PVC C900'||mat == 'PVC SCH 40'||
           mat == 'PVC SDR 14'||mat == 'PVC SDR 17'||mat == 'PVC SDR 26'||
           mat == 'PVC SDR 35'||mat == 'PVC SDR 40'||mat == 'Yelomine') {
    matAbbr = 'PVC';
} else if (mat == 'Ductile Iron') {
    matAbbr = 'DI';
} else if (mat == 'Steel') {
    matAbbr = 'STL';
 } else if (mat == 'Truss Pipe') {
    matAbbr = 'TP';
} else if (mat == 'HDPE'||mat == 'HDPE DR11'||mat=='SIDR 9 HDPE'||mat == 'PE') {
    matAbbr = 'HDPE';
}else {
    matAbbr = 'UNK'; // Unknown material
}

return diam + " " + matAbbr;
