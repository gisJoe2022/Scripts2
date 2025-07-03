// This script is used to generate a label for water lines based on their diameter and material.
// It assigns a specific abbreviation for each material type and combines it with the diameter.
// Author: Joe Hayes
// Date: 2025-04-15
// Version: 1.0
// This script is intended to be used in ArcGIS Online or ArcGIS Enterprise as a label expression.


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
} else if (mat == 'Galvanized Steel') {
    matAbbr = 'Gal';
} else if (mat == 'Clay') {
    matAbbr = 'TC';
} else if (mat == 'Concrete') {
    matAbbr = 'CON';
} else if (mat == 'Copper') {
    matAbbr = 'CPR';
} else if (mat == 'CPVC'||mat == 'PVC'||mat == 'PVC C900'||mat == 'PVC SCH 40'||
           mat == 'PVC SDR 14'||mat == 'PVC SDR 17'||mat == 'PVC SDR 26'||
           mat == 'PVC SDR 35'||mat == 'PVC SDR 40'||mat == 'Yelomine') {
    matAbbr = 'PVC';
} else if (mat == 'Ductile Iron') {
    matAbbr = 'DI';
} else if (mat == 'Steel') {
    matAbbr = 'STL';
} else if (mat == 'HDPE'||mat == 'HDPE DR11'||mat=='SIDR 9 HDPE'||mat == 'PE') {
    matAbbr = 'HDPE';
}else {
    matAbbr = 'UNK'; // Unknown material
}

return diam + " " + matAbbr;
