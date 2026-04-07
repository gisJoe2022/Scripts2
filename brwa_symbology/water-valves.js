// ===============================================
// Water Valves Symbology

// Replace these with the actual field names
var vtype = $feature.System_Valve_Type;
var vstatus = $feature.Status;

if (vtype == "Gate" && vstatus == "Active" || 
    vtype == "Gate" && vstatus == "Unknown" ||
    vtype == "Gate" && IsEmpty(vstatus))  {
    return "Gate";
}
else if (vtype == "Gate" && vstatus == "Abandoned" || vstatus == "Inactive") {
    return "Abandoned/Inactive Gate";
}
else if (vtype == "Curb Stop" && vstatus == "Active") {
    return "Curb Stop";
}
else if (vtype == "Gate" && vstatus == "Closed") {
    return "Closed Gate";
}
else if (vtype == "Butterfly" && vstatus == "Active") {
    return "Butterfly";
}
else if (vtype == "Flushing Gate Valve" && vstatus == "Active") {
    return "Flushing Gate Valve";
}
else if (vtype == "Ball" && vstatus == "Active") {
    return "Ball";
}
else if (vtype == "Inserta Valve" ) {
    return "Inserta";
}
else if (vtype == "Cone") {
    return "Cone";
}
else if (vtype == "Pinch Valve") {
    return "Pinch";
}
else if (vtype == "Corp Stop") {
    return "Corp Stop";
}
else if (vtype == "Post Indicator Valve") {
    return "Post Indicator";
}


/* var vtype = $feature.System_Valve_Type;
var vstatus = $feature.Status;

var key = vtype + "-" + (vstatus || "");

switch (key) {
    case "Gate-Active":
    case "Gate-Unknown":
    case "Gate-":
        return "Gate";
    case "Curb Stop-Active":
        return "Curb Stop";
    case "Gate-Closed":
        return "Closed Gate";
    case "Butterfly-Active":
        return "Butterfly";
    case "Flushing Gate Valve-Active":
        return "Flushing Gate Valve";
    case "Ball-Active":
        return "Ball";
    case "Cone-Active":
        return "Cone";
    default:
        if (vtype == "Inserta Valve") {
            return "Inserta";
        }
        return "------";
} */