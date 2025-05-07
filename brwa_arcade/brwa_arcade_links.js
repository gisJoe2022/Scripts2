// gravity main sewer feature service
// Description: This Arcade expression generates a URL.
// The URL is constructed using the CGID and catograph url.
// the cgid is exported from cartegraph, jointed to feature service, used to calc new GIS feild.
// author: joe hayes
// date: 2023-10-03

var cgid = $feature.cgid
var url1 = "https://bedfordrwava.eam.opengov.com/index-map/(side-panel:detail/SewerGravityMainsClass/"
var url2 = ")?area=Assets"

url1 + cgid + url2


// manholes link
var cgid = $feature.cgid
var url1 = "https://bedfordrwava.eam.opengov.com/index-map/(side-panel:detail/cgSewerManholesClass/"
var url2 = ")?area=Assets"

url1 + cgid + url2

