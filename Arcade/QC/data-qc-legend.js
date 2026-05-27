

// layer symbology for meter qc layer. this is used to color 
// code the points based on missing attributes.
// joe hayes January 2026
var installdate = $feature.Install_Date
var metertype = $feature.Meter_Type
var diam = $feature.Diameter
var read = $feature.Read_Type
var prem = $feature.Premise
var mnum = $feature.Meter_Number

if (metertype != "Empty Yoke" && IsEmpty(installdate)){
    return "Missing Install Date"
}
else if (metertype != "Empty Yoke" && IsEmpty(diam)){
    return "Missing Diameter"
}
else if (metertype != "Empty Yoke" && IsEmpty(read)){
    return "Missing Read Type"
}
else if (metertype != "Empty Yoke" && IsEmpty(prem)){
    return "Missing Premise"
}
else if (metertype != "Empty Yoke" && IsEmpty(mnum)){
    return "Missing Meter Number"
}
else{
    ""
}

// layer symbology for gravisty main sewer qc layer. 
var inst = $feature.Install_Date
var mat = $feature.Material
var diam = $feature.Diameter
//var ty = $feature.Ftype

if (IsEmpty(inst)){
    return "Missing Install Date"
}
else if (IsEmpty(diam)){
    return "Missing Diameter"
}
else if (IsEmpty(mat)){
    return "Missing Material"
}
