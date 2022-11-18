var portal = Portal("https://www.arcgis.com/");
// Create a FeatureSet for each manufacturer Feature Layer containing vaccination allocation data. 
// Group the features by the week of allocation 
var lines = GroupBy(
  //FeatureSetByPortalItem(portal,"20a80cd89db74c568db7cc9d2a13dc27",0,["*"],false),
  FeatureSetById($map,'MSTIP Opp Fund Projects', ['*'], true);
  ["week_of_allocations"],
  [
    { name: "MSTIP", expression: "MSTIPOPP_Amount2", statistic: "SUM" },
    { name: "Total", expression: "TotalProjectAmount2", statistic: "SUM" },
  ]
);

// var pfizer = GroupBy(
//   FeatureSetByPortalItem(portal,"45c991b4fd6642be8256a6b55f809311",0,["*"],false),
//   ["week_of_allocations"],
//   [
//     { name: "pfizer_1", expression: "F_1st_dose_allocations", statistic: "SUM" },
//     { name: "pfizer_2", expression: "	F_2nd_dose_allocations", statistic: "SUM" },
//   ]
// );

// var janssen = GroupBy(
//   FeatureSetByPortalItem(portal,"d6bf72497e7e4bc69ef9c468e362ca3b",0,["*"],false),
//   ["week_of_allocations"],
//   [{ name: "janssen", expression: "F_1st_dose_allocations", statistic: "SUM" }]
// );

var combinedDict = {
  fields: [
    { name: "Prject_Name", type: "esriFieldTypeString" },
    { name: "WCCC_Approval", type: "esriFieldTypeString" },
    { name: "Status", type: "esriFieldTypeString" },
    { name: "ProjectType", type: "esriFieldTypeString" },
    { name: "ProjectType2", type: "esriFieldTypeString" },
    { name: "MSTIPOPP_Amount2", type: "esriFieldTypeInteger" },
    { name: "TotalProjectAMount2", type: "esriFieldTypeInteger" },
    { name: "CommDistrict1", type: "esriFieldTypeString" },
  ],
  geometryType: "",
  features: [],
};

// Loop through each of the three FeatureSets and store attributes into a combined dictionary.
var i = 0;
for (var m in lines) {
  combinedDict.features[i] = {
    attributes: {
      manufacturer: "Moderna",
      week_of_allocation: m["week_of_allocations"],
      count_of_doses: SUM(m["MSTIP"], m["Total"]),
    },
  };
  i++;
}

// for (var p in pfizer) {
//   combinedDict.features[i] = {
//     attributes: {
//       manufacturer: "Pfizer",
//       week_of_allocation: p["week_of_allocations"],
//       count_of_doses: SUM(p["pfizer_1"], p["pfizer_2"]),
//     },
//   };
//   i++;
// }

// for (var j in janssen) {
//   combinedDict.features[i] = {
//     attributes: {
//       manufacturer: "Janssen",
//       week_of_allocation: j["week_of_allocations"],
//       count_of_doses: j["janssen"],
//     },
//   };
//   i++;
// }

// Return dictionary cast as a feature set 
return FeatureSet(Text(combinedDict));