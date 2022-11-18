
//popups

//emergency
var checkvalue = $feature.TYPE
var img_blank = ''
var img_roadsb = 'https://washcomultimedia.s3.amazonaws.com/CMSBigFiles/Wc-roads+Emergency+Icon.png'
iif(checkvalue=='Emergency',img_roadsb,img_blank)

//long term
var checkvalue = $feature.TYPE
var img_blank = ''
var img_roadsb = 'https://washcomultimedia.s3.amazonaws.com/CMSBigFiles/Wc-roads+Long-Term+Icon.png'
iif(checkvalue=='Long Term',img_roadsb,img_blank)

//short term
var checkvalue = $feature.TYPE
var img_blank = ''
var img_roadsb = 'https://washcomultimedia.s3.amazonaws.com/CMSBigFiles/Wc-roads+Short-Term+Icon.png'
iif(checkvalue=='Short Term',img_roadsb,img_blank)

//upcoming
var checkvalue = $feature.TYPE
var img_blank = ''
var img_roadsb = 'https://washcomultimedia.s3.amazonaws.com/CMSBigFiles/Wc-roads+Upcoming+Icon.png'
iif(checkvalue=='Upcoming',img_roadsb,img_blank)

//snow zone
var checkvalue = $feature.TYPE
var img_blank = ''
var img_roadsb = 'https://washcomultimedia.s3.amazonaws.com/CMSBigFiles/Wc-roads+Snow+Zone+Icon.png'
iif(checkvalue=='SnowZone',img_roadsb,img_blank)
