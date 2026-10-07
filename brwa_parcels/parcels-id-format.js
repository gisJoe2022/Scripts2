


var p = Trim($feature.Parcel_Number);

p = Replace(p, "     ", " ");
p = Replace(p, "    ", " ");
p = Replace(p, "   ", " ");
p = Replace(p, "  ", " ");

Replace(p, " ", "-")


____________________________________________________________________________

// 1. Guard against empty or null fields to prevent execution errors
if (IsEmpty($feature.Date_)) {
    return null;
}

// 2. Parse the non-standard text string using its exact matching layout
// Change 'MM/DD/YYYY' to match your specific layout (e.g., 'DD-MM-YYYY')
var fullDate = Date($feature.Date_, 'MM/DD/YYYY');

// 3. Cast the full date object down into a pure DateOnly data type
return DateOnly(fullDate);