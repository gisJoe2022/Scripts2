var seURL = 'https://gisims.co.washington.or.us/GIS/Survey/se2/SurveyExplorer.html';

columnValues = {
    "default": {
        "data": [],
        "label": []
    },
    "search-survey": {
        "data": [
            {
                "data": "Surveynumber",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a uid="' + data + '" class="data-modal" target="_blank" href="../#/view/' + data + '">' + data + '</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            {
                "data": "Surveynumber",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a class="mapview" target="_blank" href="' + seURL + '?type=survey&searchString=' + data + '">View</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            { "data": "Surveyorname"},
            { "data": "WASHCO_COMPANYNAME"},
            { "data": "Client"},
            {
                "data": "Date_Survey",
                "type": "date",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var newDate = moment(data.date).format("M/D/YYYY");
                        return newDate;
                    } else {
                        return '';
                    }
                }
            },
            {
                "data": "Filed",
                "type": "date",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var newDate = moment(data.date).format("M/D/YYYY");
                        return newDate;
                    } else {
                        return '';
                    }
                }
            },
            {
                "data": "TRSQTR",
                "orderable": false,
                "render": function(data, type, full, meta) {
                    if (data) {
                        
                        var view = '';
                        $.each(data, function(index, value) {
                            var isMultiple = (index > 0) ? ',<br>' : '';
                            view += isMultiple + value;
                        });
                        return view;
                    } else {
                        return '';
                    }
                }
            },
        ],
        "label": [
            { "title": "Survey Number"},
            { "title": "Map"},
            { "title": "Surveyor"},
            { "title": "Business"},
            { "title": "Client"},
            { "title": "Date of Survey"},
            { "title": "Filed Date"},
            { "title": "Township/Range/Section"}
        ]
    },
    "search-benchmark": {
        "data": [
            {
                "data": "ID",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a uid="' + data + '" class="data-modal" target="_blank" href="../#/view/' + data + '">' + data + '</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            {
                "data": "ID",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a class="mapview" target="_blank" href="' + seURL + '?type=benchmark&searchString=' + data + '">View</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            { "data": "STAMPING"},
            {
                "data": "TR",
                "orderable": false, 
                "render": function(data, type, row) {
                    if (data) {
                        var view = data + row['Sec']  + row['QTR'];
                        return view;
                    } else {
                        return '';
                    }
                }
            },
            { "data": "ELEVATION1"}
           
        ],
        "label": [
            { "title": "Benchmark ID"},
            { "title": "Map"},
            { "title": "Stamping"},
            { "title": "TRSQTR"},
            { "title": "Elevation"},
            
        ]
    },
    "search-corner": {
        "data": [
            {
                "data": "CORNERID",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a uid="' + data + '" class="data-modal" target="_blank" href="../#/view/' + data + '">' + data + '</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            {
                "data": "CORNERID",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a class="mapview" target="_blank" href="' + seURL + '?type=publiclandcorner&searchString=' + data + '">View</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            {
                "data": "BookPage",
                "render": function(data, type, full, meta) {
                    if (data) {
                        
                        var view = '';
                        $.each(data, function(index, value) {
                            var isMultiple = (index > 0) ? ',<br>' : '';
                            view += isMultiple + value;
                        });
                        return view;
                    } else {
                        return '';
                    }
                }
            },
            { "data": "GPS_ID" },
            {
                "data": "DESCRIPTION",
                "render": function(data, type, full, meta) {
                    if (data) {
                        
                        var view = data[0];
                        return view;
                    } else {
                        return '';
                    }
                }
            }
           
        ],
        "label": [
            { "title": "Corner ID"},
            { "title": "Map"},
            { "title": "Book/Page"},
            { "title": "GPS ID"},
            { "title": "Description"},
            
        ]
    },
    "search-geocontrol": {
        "data": [
            {
                "data": "Fullname",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a uid="' + data + '" class="data-modal" target="_blank" href="../#/view/' + data + '">' + data + '</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            {
                "data": "Fullname",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a class="mapview" target="_blank" href="' + seURL + '?type=geodesiccontrol&searchString=' + data + '">View</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            { "data": "Name" },
            { "data": "Latitude" },
            { "data": "Longitude" },
            { "data": "DESCRIPTION" },
           
        ],
        "label": [
            { "title": "Full Name"},
            { "title": "Map"},
            { "title": "Name"},
            { "title": "Latitude"},
            { "title": "Longitude"},
            { "title": "Description"},
            
        ]
    },
    "search-plat": {
        "data": [
            {
                "data": "Platname",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a uid="' + data + '" class="data-modal" target="_blank" href="../#/view/' + data + '">' + data + '</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            {
                "data": "Platname",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a class="mapview" target="_blank" href="' + seURL + '?type=plat&searchString=' + data + '">View</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            { "data": "SurveyorName" },
            { "data": "BusinessName" },
            { "data": "Declarant" },
            {
                "data": "Recorded",
                "type": "date",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var newDate = moment(data.date).format("M/D/YYYY");
                        return newDate;
                    } else {
                        return '';
                    }
                }
            },
            { "data": "CityName" },
            { "data": "BookPage" },
            { "data": "DocNumber" }
           
        ],
        "label": [
            { "title": "Plat Name" },
            { "title": "Map" },
            { "title": "Surveyor" },
            { "title": "Business" },
            { "title": "Declarant" },
            { "title": "Recorded" },
            { "title": "City" },
            { "title": "Book/Page" },
            { "title": "Doc Number" }
            
        ]
    },
    "search-taxmap": {
        "data": [
            {
                "data": "tlid",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a uid="' + data + '" class="data-modal" target="_blank" href="../#/view/' + data + '">' + data + '</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            {
                "data": "tlid",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a class="mapview" target="_blank" href="' + seURL + '?type=taxlot&searchString=' + data + '">View</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            { "data": "OwnerName" },
            { "data": "Fulladdress" },
            { "data": "LandVal" },
            { "data": "BldgVal" },
            { "data": "TotalVal" },
            { "data": "YearBuilt" }
           
        ],
        "label": [
            { "title": "TaxlotID" },
            { "title": "Map"},
            { "title": "Owner" },
            { "title": "Situs Address" },
            { "title": "Land Value" },
            { "title": "Improvement Value" },
            { "title": "Total Value" },
            { "title": "Year Built" }
            
        ]
    },
    "search-countyroad": {
        "data": [
            {
                "data": "CROAD_ID",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a uid="' + data + '" class="data-modal" target="_blank" href="../#/view/' + data + '">' + data + '</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
            { "data": "Date" },
            { "data": "COMMENTS" },
            { "data": "COMMENTS2" },
        ],
        "label": [
            { "title": "Road ID" },
            { "title": "Date" },
            { "title": "Comments" },
            { "title": "Additional Comments" },
            
        ]
    },
    "search-smaps": {
        "data": [
            {
                "data": "url",
                "render": function(data, type, full, meta) {
                    if (data) {
                        var view = '<a target="_blank" href="' + data + '">View Map</a>';
                        return view;
                    } else {
                        return '--';
                    }
                }
            },
        ],
        "label": [
            { "title": "Image" }
            
        ]
    }
}

var onAJAXLoad = function(url, target){

    /*Remove non-returned Columns*/

    var coltarget = columnValues[urlParams.searchby];

    for (var i = 0; i < coltarget['data'].length; i++) {

        var key = coltarget['data'][i]['data'];
        var firstRow = jsonData.data[0];

        if (jsonData.data[0] && !(key in firstRow)) {
            coltarget['label'].splice(i, 1);
            coltarget['data'].splice(i, 1);
        }

    }

}

var onTableLoad = function () {
    var autoSearches = ['search-survey', 'search-benchmark', 'search-corner', 'search-geocontrol', 'search-plat', 'search-taxmap', 'search-countyroad'];
    // if (($.inArray(urlParams.searchby, autoSearches) > -1) && table.rows().count() == 1){
    //     $('a.data-modal').click();
    // }
}

var formatUOList = function(data){
    var view = '';
    var dataLen = data.length;
    if (dataLen > 0) {
        $.each(data, function(index, value) {
            if (value && dataLen > 1){
                view += "<li>" + value + "</li>";
            }
            else if (value && dataLen == 1){
                view = value;
            }
        });
        var isMultiple = (dataLen > 1) ? 'ul' : 'span';
        return '<' + isMultiple + '>' + view + '</' + isMultiple + '>';
    }
    else {
        return '<span>N/A</span>';
    }
}

// use functions to customize the data view for the modal window, otherwise just enter a title.
var dataTransform = {
    "search-survey": {
        "Date_Survey": function(data){
            var view = data.Date_Survey ? moment(data.Date_Survey.date).format("M/D/YYYY") : '';
            return '<div><b>Survey Date: </b> <span>' + view + '</span></div>';
        },
        "Surveyornumber": "Surveyor Number",
        "Surveyorname": "Surveyor",
        "TRSQTR": function(data){
            var view = '';
            if (data.TRSQTR.length > 0) {
                $.each(data.TRSQTR, function(index, value) {
                    if (value){
                        var isMultiple = (index > 0) ? ', ' : '';
                        view += isMultiple + value;
                    }
                });
            }
            return '<div><b>Town/Section/Range: </b> <span>' + view + '</span></div>';
        },
        "Received": function(data){
            var view = data.Received ? moment(data.Received.date).format("M/D/YYYY") : 'N/A';
            return '<div><b>Received: </b> <span>' + view + '</span></div>';
        },
        "Client": "Client",
        "Filed": function(data){
            var view = data.Filed ? moment(data.Filed.date).format("M/D/YYYY") : 'N/A';
            return '<div><b>Filed: </b> <span>' + view + '</span></div>';
        },
        "WASHCO_COMPANYNAME": "Company Name",
        "filename": function(data){
            var view = '';
            var dataLen = data.filename.length;

            // Grab filename and extension and return pproper link
            var fileName = function(file){
                file = file.split('.');
                file = {
                    "name": file[0],
                    "ext": file[1]
                }

                var uid = data.Surveynumber;
                var recordFolder = 0;
                var isPDF = (file['ext'].toUpperCase() == "PDF") ? '.' + file['ext'] : '';

                var imgURL = (isPDF) ? 'http://mtbachelor.co.washington.or.us/images/survey/surveys/' : 'http://mtbachelor.co.washington.or.us/images/pdfbuilderasp/tiff2pdf.asp?doctype=surveys&imageto=';

                switch (true) {
                    case (uid <= 5000):
                        recordFolder = 5000;
                        break;
                    case (uid <= 10000):
                        recordFolder = 10000;
                        break;
                    case (uid <= 15000):
                        recordFolder = 15000;
                        break;
                    case (uid <= 20000):
                        recordFolder = 20000;
                        break;
                    case (uid <= 25000):
                        recordFolder = 25000;
                        break;
                    case (uid <= 30000):
                        recordFolder = 30000;
                        break;
                    case (uid <= 35000):
                        recordFolder = 35000;
                        break;
                    case (uid <= 40000):
                        recordFolder = 40000;
                        break;
                    case (uid <= 45000):
                        recordFolder = 45000;
                        break;
                }

                var link = '<a href="' + imgURL + recordFolder + '/' + file['name'] + isPDF + '" target="_blank">' + file['name'] + '</a>';
                return link;
            }

            var dataTransform = [];

            $.each(data.filename, function(index, value) {
                dataTransform.push(fileName(value));
            });

            var view = formatUOList(dataTransform);
            return '<div><b>Images: </b>' + view + '</div>';
        }
    },
    "search-benchmark": {
        "monument": "Monument",
        "STAMPING": "Stamping",
        "Tile_Name": "TRS",
        "city": "City",
        "county": "County",
        "state": "State",
        "ELEVATION1": "Elevation",
        "established_by": "Established By",
        "Date_established": "Date Established",
        "location": "Location",
        "ref1": "Reference 1",
        "ref2": "Reference 2",
        "ref3": "Reference 3",
        "ref4": "Reference 4",
        "ref5": "Reference 5",
        "ref6": "Reference 6",
        "checked_on2001": function(data){
            var view = data.checked_on2001 ? moment(data.checked_on2001.date).format("M/D/YYYY") : 'N/A';
            return '<div><b>Checked Date: </b> <span>' + view + '</span></div>';
        },
        "checked_by2001": "Checked By",
        "condition2001": "Condition",
        "cornerid": "Corner ID",
        "gcname": "GC Name",
        "bm_site_photo": function(data){
            var view = data.bm_site_photo ? '<a target="_blank" href="' + data.BmPhoto + '">View</a>' : 'N/A';
            return '<div><b>Site Photo: </b> <span>' + view + '</span></div>';
        },
    },
    "search-corner": {
        "BLMNO": "BLM Number",
        "BOOK_PAGE_ENTRY": function(data){
            var view = formatUOList(data.BOOK_PAGE_ENTRY);
            return '<div><b>Book/Page: </b>' + view + '</div>';
        },
        "DESCRIPTION": function(data){
            var view = formatUOList(data.DESCRIPTION);
            return '<div><b>Description: </b>' + view + '</div>';
        },
        "STATUSDATE": function(data){
            var dataTransform = [];

            $.each(data.STATUSDATE, function(index, value) {
                if (value.date){
                    dataTransform.push(moment(value.date).format("M/D/YYYY"));
                }
            });

            var view = formatUOList(dataTransform);
            return '<div><b>Status Date: </b>' + view + '</div>';
        },
        "SURVEYORNUMBER": function(data){
            var view = formatUOList(data.SURVEYORNUMBER);
            return '<div><b>Surveyor Number: </b>' + view + '</div>';
        },
        "Surveyorname": function(data){
            var view = formatUOList(data.Surveyorname);
            return '<div><b>Surveyor Name: </b>' + view + '</div>';
        },
        // FIX
        "Photo_name": function(data){
            var view = data.Photo_name ? '<a target="_blank" href="' + data.sitePhoto + '">View</a>' : 'N/A';
            return '<div><b>Site Photo: </b> <span>' + view + '</span></div>';
        },
        "filename": function(data){
            var view = '';
            var dataLen = data.filename.length;

            // Grab filename and extension and return pproper link
            var fileName = function(file){
                file = file.split('.');
                file = {
                    "name": file[0],
                    "ext": file[1]
                }
                var isPDF = (file['ext'].toUpperCase() == "PDF") ? '.' + file['ext'] : '';

                var imgURL = (isPDF) ? 'http://mtbachelor.co.washington.or.us/images/survey/BTBOOKS/' : 'http://mtbachelor.co.washington.or.us/images/pdfbuilderasp/tiff2pdf.asp?doctype=btbooks&imageto=';

                var link = '<a href="' + imgURL + file['name'] + isPDF + '" target="_blank">' + file['name'] + '</a>';
                return link;
            }

            var dataTransform = [];

            $.each(data.filename, function(index, value) {
                dataTransform.push(fileName(value));
            });

            var view = formatUOList(dataTransform);
            return '<div><b>Images: </b>' + view + '</div>';
        }
    },
    "search-geocontrol": {
        "Fullname": "Geodetic Control Name",
        "stationnumber": "Station Number",
        "Latitude": "Latitude",
        "Longitude": "Longitude",
        "northfeet": "Northing (Feet)",
        "eastfeet": "Easting (Feet)",
        "northmeter": "Northing (Meter)",
        "eastmeter": "Easting (Meter)",

        "TR": function(data){
            var tr = data.TR ? data.TR + 'W' : 'N/A',
            sec = data.Sec ? data.Sec : 'N/A',
            qtr = data.QTR ? data.QTR : 'N/A';
            return '<div><b>Town/Section/Range: </b> <span>' + tr + sec + qtr + '</span></div>';
        },

        "grid_scale": "Grid Scale",
        "convergenc": "Convergence",
        "ellipsoid": "Ellipsoid",
        "govcorn": "Gov. Corner",
        "DESCRIPTION": "Description",
        "method": "Method",
        "projection": "Projection",
        "corner_id": "Corner ID",

        "accepted": function(data){
            var view = (data.accepted == 0) ? 'No' : 'Yes';
            return '<div><b>Accepted: </b> <span>' + view + '</span></div>';
        },
        "condition": "Condition",
        "surveyornumber": "Surveyor Number",
        "surveyorname": "Surveyor Name",
        "filename": function(data){
            var view = '';
            var dataLen = data.filename.length;

            // Grab filename and extension and return pproper link
            var fileName = function(file){
                file = file.split('.');
                file = {
                    "name": file[0],
                    "ext": file[1]
                }
                var isPDF = (file['ext'].toUpperCase() == "PDF") ? '.' + file['ext'] : '';

                var imgURL = (isPDF) ? 'http://mtbachelor.co.washington.or.us/images/survey/control/' : 'http://mtbachelor.co.washington.or.us/images/pdfbuilderasp/tiff2pdf.asp?doctype=control&imageto=';
                var link = '<a href="' + imgURL + file['name'] + isPDF + '" target="_blank">' + file['name'] + '</a>';
                return link;
            }

            var dataTransform = [];

            $.each(data.filename, function(index, value) {
                dataTransform.push(fileName(value));
            });

            var view = formatUOList(dataTransform);
            return '<div><b>Images: </b>' + view + '</div>';
        }
    },
    "search-plat": {
        "Recorded": function(data){
            var view = data.Recorded ? moment(data.Recorded.date).format("M/D/YYYY") : 'N/A';
            return '<div><b>Checked Date: </b> <span>' + view + '</span></div>';
        },
        "Surveyornumber": "Surveyor Number",
        "SurveyorName": "Surveyor Name",
        "TR": function(data){
            var tr = data.TR ? data.TR + 'W' : 'N/A',
            sec = data.Sec ? data.Sec : 'N/A',
            qtr = data.QTR ? data.QTR : 'N/A';
            return '<div><b>Town/Section/Range: </b> <span>' + tr + sec + qtr + '</span></div>';
        },
        "Declarant": "Declarant",
        "Lots": "Lots",
        "Tracts": "Tracts",
        "BusinessName": "Business Name",
        "CityName": "City",
        "BOOKPAGE": "Book/Page",
        "DocNumber": "Doc Number",
        "filename": function(data){
            var view = '';
            var dataLen = data.filename.length;

            // Grab filename and extension and return pproper link
            var fileName = function(file){
                file = file.split('.');
                file = {
                    "name": file[0],
                    "ext": file[1]
                }


                var uid = data.Platname[0];
                var recordFolder = 0;
                var isPDF = (file['ext'].toUpperCase() == "PDF") ? '.' + file['ext'] : '';

                // If first character of uid is not a number:
                if (isNaN(uid)){
                    switch (true) {
                        case (uid <= 'E'):
                            recordFolder = 'PltsAtoE';
                            break;
                        case (uid <= 'L'):
                            recordFolder = 'PltsFtoL';
                            break;
                        case (uid <= 'S'):
                            recordFolder = 'PltsMtoS';
                            break;
                        case (uid <= 'Z'):
                            recordFolder = 'PltsTtoZ';
                            break;
                    }
                }
                else {
                    recordFolder = 'Plts1to9';
                }

                var imgURL = (isPDF) ? 'http://mtbachelor.co.washington.or.us/images/survey/plats/' : 'http://mtbachelor.co.washington.or.us/images/pdfbuilderasp/tiff2pdf.asp?doctype=plats&imageto=';
                var link = '<a href="' + imgURL + recordFolder + '/' + file['name'] + isPDF + '" target="_blank">' + file['name'] + '</a>';
                return link;
            }

            var dataTransform = [];

            $.each(data.filename, function(index, value) {
                dataTransform.push(fileName(value));
            });

            var view = formatUOList(dataTransform);
            return '<div><b>Images: </b>' + view + '</div>';
        }
    },
    "search-taxmap": {
        "tlid": function(data){
            var view = data.tlid ? '<a target="_blank" href="http://gisims.co.washington.or.us/GIS/index.cfm?id=20&sid=3&IDValue=' + data.tlid + '">InterMap</a>' : 'N/A';
            return '<div><b>More Info: </b> <span>' + view + '</span></div>';
        },
        "OwnerName": function(data){
            var OwnerName = data.OwnerName ? data.OwnerName : '',
            OwnerAddr = data.OwnerAddr ? '<br>' + data.OwnerAddr : '',
            OwnerAddr2 = data.OwnerAddr2 ? '<br>' + data.OwnerAddr2 : '',
            OwnerAddr3 = data.OwnerAddr3 ? '<br>' + data.OwnerAddr3 : '',
            OwnerCity = data.OwnerCity ? '<br>' + data.OwnerCity : '',
            OwnerState = data.OwnerState ? ', ' + data.OwnerState : '',
            OwnerZip = data.OwnerZip ? ' ' + data.OwnerZip : '';
            return '<div><b>Property Owner: </b> <span>' + OwnerName + OwnerAddr + OwnerAddr2 + OwnerAddr3 + OwnerCity + OwnerState + OwnerZip + '</span></div>';
        },

        "Site Address": "Site Address",
        "LandVal": "Land Value",
        "BldgVal": "Building Value",
        "TotalVal": "Total Value",
        "BldgSqft": "Bldg Sq Ft",
        "Acres": "Acres",
        "YearBuilt": "Year Built",
        "SaleDate": "Sale Date",
        "SalePrice": "Sale Price",
        "Account": "Account",
        "filename": function(data){
            var view = '';
            var dataLen = data.filename.length;

            // Grab filename and extension and return pproper link
            var fileName = function(file){

                var link = '<a href="http://mtbachelor.co.washington.or.us/images/pdfbuilderasp/tiff2pdf.asp?doctype=taxmaps&imageto=' + file.TaxmapBW + '" target="_blank">' + file.MapType + '</a>';
                return link;
            }

            var dataTransform = [];

            $.each(data.filename, function(index, value) {
                dataTransform.push(fileName(value));
            });

            var view = formatUOList(dataTransform);
            return '<div><b>Images: </b>' + view + '</div>';
        }
    },
    "search-countyroad": {
        "CROAD_ID": "Road ID",
        "Date": "Date",
        "COMMENTS": "Comments",
        "COMMENTS2": "Additional Comments",
        "filename": function(data){
            var view = '';
            var dataLen = data.filename.length;

            // Grab filename and extension and return pproper link
            var fileName = function(file){
                file = file.split('.');
                file = {
                    "name": file[0],
                    "ext": file[1]
                }
                var isPDF = (file['ext'].toUpperCase() == "PDF") ? '.' + file['ext'] : '';

                var imgURL = (isPDF) ? 'http://mtbachelor.co.washington.or.us/images/survey/CoRoads/' : 'http://mtbachelor.co.washington.or.us/images/pdfbuilderasp/tiff2pdf.asp?doctype=coroads&imageto=';
                var link = '<a href="' + imgURL + file['name'] + isPDF + '" target="_blank">' + file['name'] + '</a>';
                return link;
            }

            var dataTransform = [];

            $.each(data.filename, function(index, value) {
                dataTransform.push(fileName(value));
            });

            var view = formatUOList(dataTransform);
            return '<div><b>Images: </b>' + view + '</div>';
        }
    }
}

var popHeader = {
    "search-survey": function(uid){
        var view = uid ? uid : '';
        return '<h1>Survey ' + uid + '</h1>';
    },
    "search-benchmark": function(uid){
        var view = uid ? uid : '';
        return '<h1>Benchmark ' + uid + '</h1>';
    },
    "search-corner": function(uid){
        var view = uid ? uid : '';
        return '<h1>Public Land Corner ' + uid + '</h1>';
    },
    "search-geocontrol": function(uid){
        var view = uid ? uid : '';
        return '<h1>Control ' + uid + '</h1>';
    },
    "search-plat": function(uid){
        var view = uid ? uid : '';
        return '<h1>Plat ' + uid + '</h1>';
    },
    "search-taxmap": function(uid){
        var view = uid ? uid : '';
        return '<h1>Taxlot ' + uid + '</h1>';
    },
    "search-countyroad": function(uid){
        var view = uid ? uid : '';
        return '<h1>Road ' + uid + '</h1>';
    }
}

var setRecord = function(data, searchBy, uid){

    // Clear Existing Modal Items
    $('#modal-window #modal-content .popHeader').html('');
    $('#modal-window #modal-content .items').html('');

    // Setup Header
    if (popHeader[searchBy]){
        $('#modal-window #modal-content .popHeader').append(popHeader[searchBy](uid));
    }

    console.log(data);

    // Setup Items
    if (dataTransform[searchBy]){
        $.each(dataTransform[searchBy], function(index, value) {

            if (index in data) {

                var view = '';
                if (typeof value === 'function'){
                    view = value(data, uid);
                }
                else {
                    var dataval = data[index] ? data[index] : 'N/A';
                    view = '<div><b>' + value + ': </b> <span>' + dataval + '</span></div>';
                }

                $('#modal-window #modal-content .items').append(view);
            }

        });
    }

    $('#modal-window').modal();
}

var requestIDRecord = function(uid) {
    var searchBy = urlParams['searchby'];
    $.jsonp({
        type: "GET",
        url: baseURL + '/services/survey/id/?type=' + searchBy + '&uid=' + uid,
        cache: false,
        callbackParameter: "callback",

        success: function(json) {
            if (!json.data.error) {
                $('.error-message').text('').addClass('hidden');
                setRecord(json.data[0], searchBy, uid);
            } else {
               $('#modal-window #modal-content .popHeader').html('<h1>Error</h1>');
               $('#modal-window #modal-content .items').html('<p><b>Record not found.</b></p>');
               $('#modal-window').modal();
            }
        },
        error: function(xhr, textStatus, errorThrown) {},
        complete: function(xOptions, textStatus) {
            $body.removeClass("loading");
        },
        beforeSend: function(xOptions) {
            $body.addClass("loading");
        }
    });

    // var record = table.row(elm.parents('tr')).data();
    // setRecord(record);

}


$(document).ready(function() {

    $( ".datepicker" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "yy-mm-dd"
    });

    //On Search By Input Change
    $('#surveyReport #searchby').on('change', function() {
        var search = this.value || '';
        var inputItems = $('#surveyReport .input-item');

        $.each(inputItems, function(index, value) {
            if ($(value).hasClass(search)) {
                $(value).removeClass('hidden');
                $(value).find("input").attr("disabled", false);
                $(value).find("select").attr("disabled", false);
            } else {
                $(value).find("input").attr("disabled", true);
                $(value).find("select").attr("disabled", true);
                $(value).addClass('hidden');
            }
        });
    });

    /*Grab Data for Surveyor Names*/
    $.jsonp({
        type: "GET",
        url: baseURL + "/services/survey/input",
        cache: false,
        callbackParameter: "callback",

        success: function(json) {


            // If data returns, change input element to select and populate with options.
            if (!json.data.error) {
                $('.error-message').text('').addClass('hidden');

                // Setup Surveyor Names
                if (json.data.surveyorname){
                    $( "#surveyReport #input-surveyorname input" ).autocomplete({
                        source: json.data.surveyorname,
                        minLength: 2,
                        focus: function( event, ui ) {
                            $( "#surveyReport #input-surveyorname input" ).val( ui.item.label );
                            return false;
                        },
                    });
                }

                // Setup Business Names
                if (json.data.businessname){
                    $( "#surveyReport #input-businessname input" ).autocomplete({
                        source: json.data.businessname,
                        minLength: 2,
                        focus: function( event, ui ) {
                            $( "#surveyReport #input-businessname input" ).val( ui.item.label );
                            return false;
                        },
                    });
                }
            }

        },
        error: function(xOptions, textStatus) {

        },
        complete: function(xOptions, textStatus) {
            $body.removeClass("loading");

            //Setup existing URL params
            urlParams = getAllUrlParams();
            if (!$.isEmptyObject(urlParams)) {
                $.each(urlParams, function(index, value) {
                    if (value) {
                        // Replace '+'' symbols with ' '
                        value = value.replace(/\+/g, '%20')
                        $('#surveyReport #' + index).val(decodeURIComponent(value)).change();
                    }
                });
            }

            // Auto create tables if account or tax lot number is given
            var url = baseURL + '/services/survey/search/?' + $.param(urlParams);
            if (urlParams['surveynumber'] || urlParams['benchmarkid'] || urlParams['cornerid'] || urlParams['controlname'] || urlParams['platname']){
                createTable(url, true);
            }
            else {
                createTable();
            }

        },
        beforeSend: function(xOptions) {
            $body.addClass("loading");
        }
    });

    // On Submit of Search
    $("#surveyReport").submit(function(event) {

        urlParams = {};
        $.each($("#surveyReport").serializeArray(), function(i, field) {
            if (field.value) {
                urlParams[field.name] = field.value;
            }
        });
        var url = baseURL + '/services/survey/search/?' + $.param(urlParams);
        window.location.replace("#/?" + $.param(urlParams));
        table.destroy();
        $('.datatable').empty();
        createTable(url, true);
        event.preventDefault();
    });

    $("#search-clear").on('click', function(event) {
        var inputItems = $('#surveyReport .input-item');

        $.each(inputItems, function(index, value) {
            $(value).find("input").val('');
            $(value).find("select").val('');
        });
        event.preventDefault();
    });


    /*On Record Click
    Request for additional data to display*/
    $("#datatable").on('click', 'a.data-modal', function(event) {
        var uid = $(this).attr('uid');
        requestIDRecord(uid);
        event.preventDefault();
    });


    // Map Viewer
    $("#datatable").on('click', 'a.mapview', function(event) {
        var url = $(this).attr('href');
        $('#map').attr('src',url);
        var scrollTo = $('#map');
        if ($(scrollTo).length > 0){
            $('html, body').stop().animate({scrollTop: $(scrollTo).offset().top}, '1000', 'linear');
        }
        event.preventDefault();
    });



});