//interate through a set of values and 
//to get the predominate number in the set


var uvInfos = [{
    "value": "2032",
    "label": "2032"
  }, {
    "value": "2031",
    "label": "2031"
  }, {
    "value": "2030",
    "label": "2030"
  }, {
    "value": "2029",
    "label": "2029"
  }, {
    "value": "2028",
    "label": "2028"
  }, {
    "value": "2027",
    "label": "2027"
  }, {
    "value": "2026",
    "label": "2026"
  }, {
    "value": "2025",
    "label": "2025"
  }];
var predominantType = Text($feature["cluster_type_RepYear"]);
var label = "None";

for (var i = 0; i < Count(uvInfos); i++) {
if (uvInfos[i].value == predominantType) {
  label = uvInfos[i].label;
  break;
}
}

return label;