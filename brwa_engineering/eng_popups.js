// Engineering groups map popups
// joe hayes
// Bedford Regional Water Authority
// 4/1/2025

// gravity sewer main opengov link
var cgid = $feature.cgid
var url1 = "https://bedfordrwava.eam.opengov.com/index-map/(side-panel:detail/SewerGravityMainsClass/"
var url2 = ")?&area=asset"

if (cgid == null) return "https://www.dropbox.com/scl/fi/8bsv9ib2721um6uueklm4/PageNotFound.pdf" 

url1 + cgid + url2

