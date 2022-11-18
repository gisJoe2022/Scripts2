
// returns an attached image
// resulting expression is placed in the pop-up media URL+
// source - https://youtu.be/MzfxBskoon8

var Part1 = "https://gisint.co.washington.or.us/server/rest/services/LUT_ETS/Corner_Fieldnotes/FeatureServer/91/"
var ObjectID = $feature.OBJECTID
var Part2 = "/attachments/"
var AttachID = $feature.AttachID

return Part1 + ObjectID + Part2 + AttachID
