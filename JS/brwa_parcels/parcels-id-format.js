


var p = Trim($feature.Parcel_Number);

p = Replace(p, "     ", " ");
p = Replace(p, "    ", " ");
p = Replace(p, "   ", " ");
p = Replace(p, "  ", " ");

Replace(p, " ", "-")