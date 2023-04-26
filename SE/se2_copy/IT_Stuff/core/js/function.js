$body = $("body");

var baseURL = "https://api.co.washington.or.us/v1";
var table,
    columnValues,
    divTable;
var urlParams = {
    "searchby": null
};
var jsonData = {
    "data": null
}
var defaultTableSettings = {
    lengthMenu: [
        [25, 50, 100, -1],
        [25, 50, 100, "All"]
    ],
    order: []
};


//RECAPTCHA
var recaptchaKey = "6LdK0W4bAAAAAPgG5QQ7fbn-CQ_iMFTb3kO6DOhh";
var responseCapture = '';
var recaptchaLoad = function() {};
var correctCaptcha = function(response) {
    if (response){
        responseCapture = response;
    }
    else {
        responseCapture = '';
    }
};

$(document).on({
    ajaxStart: function() {
        $body.addClass("loading");
    },
    ajaxStop: function() {
        $body.removeClass("loading");
    },
    ajaxError: function() {
        $body.removeClass('loading');
    }
});

// Set Year in Footer
var d = new Date();
$('span#footeryear').text(d.getFullYear());

//URL Param Grab
var getUrlParameter = function(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
        return '';
};

var getAllUrlParams = function() {

    var url = window.location.hash.substring(1).split('/')[1];
    // get query string from url (optional) or window
    var queryString = url ? url.split('?')[1] : window.location.search.slice(1);

    // we'll store the parameters here
    var obj = {};

    // if query string exists
    if (queryString) {

        // stuff after # is not part of query string, so get rid of it
        queryString = queryString.split('#')[0];

        // split our query string into its component parts
        var arr = queryString.split('&');

        for (var i = 0; i < arr.length; i++) {
            // separate the keys and the values
            var a = arr[i].split('=');

            // set parameter name and value (use 'true' if empty)
            var paramName = a[0];
            var paramValue = typeof(a[1]) === 'undefined' ? true : a[1];

            // (optional) keep case consistent
            // paramName = paramName.toLowerCase();
            // if (typeof paramValue === 'string') paramValue = paramValue.toLowerCase();

            // if the paramName ends with square brackets, e.g. colors[] or colors[2]
            if (paramName.match(/\[(\d+)?\]$/)) {

                // create key if it doesn't exist
                var key = paramName.replace(/\[(\d+)?\]/, '');
                if (!obj[key]) obj[key] = [];

                // if it's an indexed array e.g. colors[2]
                if (paramName.match(/\[\d+\]$/)) {
                    // get the index value and add the entry at the appropriate position
                    var index = /\[(\d+)\]/.exec(paramName)[1];
                    obj[key][index] = paramValue;
                } else {
                    // otherwise add the value to the end of the array
                    obj[key].push(paramValue);
                }
            } else {
                // we're dealing with a string
                if (!obj[paramName]) {
                    // if it doesn't exist, create property
                    obj[paramName] = paramValue;
                } else if (obj[paramName] && typeof obj[paramName] === 'string') {
                    // if property does exist and it's a string, convert it to an array
                    obj[paramName] = [obj[paramName]];
                    obj[paramName].push(paramValue);
                } else {
                    // otherwise add the property
                    obj[paramName].push(paramValue);
                }
            }
        }
    }

    return obj;
}

// Create Table with AJAX URL. If autoScroll is set, the window scrolls down to table (Useful for form submissions).
// Add target value to create table in a specific div class (default is .datatable).
var createTable = function(url, autoScroll, target) {

    divTable = target ? target : ".datatable"; 

    if (url) {

        $('body form.ws-validate').find(':input[type=submit]').prop('disabled', true);

        // Check if url provided is a string. If not, it will assume it's a JSON dataset
        var urlCheck = (typeof url == "string");
        
        var loadData = function(json){
            /*Save JSON to memory*/
            jsonData = json;


            if (typeof onAJAXLoad === 'function'){
                onAJAXLoad(url, target);
            }

            if (jsonData.data.error) {

                $('.error-message').text("Error - " + json.data.error.status).removeClass('hidden');

                loadBlankTable(url, target);
                return false;
            }

            if (!jsonData.data){
                loadBlankTable(url, target);
                return false;
            }

            $('.error-message').text('').addClass('hidden');


            /*Set Data Defaults*/
            var column = columnValues[urlParams.searchby]['data'];
            $.each(column, function(index, value) {
                 value['defaultContent'] = '';
            });
            
            /*Set Label Targets*/
            var label = columnValues[urlParams.searchby]['label'];
            $.each(label, function(index, value) {
                 value['targets'] = index;
            });

            /*Set Heading Text*/
            if (columnValues[urlParams.searchby]['title']){
                $('#main-title').text(columnValues[urlParams.searchby]['title']);
            }

            var tableSettings = {
                data: jsonData.data || '',
                order: defaultTableSettings['order'],
                lengthMenu: defaultTableSettings['lengthMenu'],
                scrollX: true,
                language: {
                    search: "Filter Results:"
                },
                dom: 'Blfrtip',
                buttons: [
                    {
                        extend: 'collection',
                          text: 'Export Data',
                          className: 'btn btn-sm btn-outline-dark no-round-right',
                          buttons: [
                            {
                                extend: 'excelHtml5',
                                exportOptions: {
                                    columns: ':visible'
                                },
                                text: "Excel"
                            },
                            {
                                extend: 'csvHtml5',
                                exportOptions: {
                                    columns: ':visible'
                                },
                                text: "CSV"
                            },
                            {
                                extend: 'pdfHtml5',
                                orientation: 'portrait',
                                pageSize: 'LEGAL',
                                exportOptions: {
                                    columns: ':visible'
                                },
                                text: "PDF (Portrait)",
                                customize: function(doc) {
                                    doc.defaultStyle.fontSize = 8;
                                    doc.styles.tableHeader.fontSize = 8;
                               }  
                            },
                            {
                                extend: 'pdfHtml5',
                                orientation: 'landscape',
                                pageSize: 'LEGAL',
                                exportOptions: {
                                    columns: ':visible'
                                },
                                text: "PDF (Landscape)",
                                customize: function(doc) {
                                    doc.defaultStyle.fontSize = 8;
                                    doc.styles.tableHeader.fontSize = 8;
                               }  
                            }
                          ]
                    },
                    {
                        extend: 'colvis',
                        text: "Hide/Show Columns"
                    }
                ],
                columns: columnValues[urlParams.searchby]['data'],
                columnDefs: columnValues[urlParams.searchby]['label'],

                initComplete: function() {
                    

                    if (typeof onTableLoad === 'function'){
                        setTimeout(function(){
                            onTableLoad(url, target);
                        }, 500);
                    }

                    if (autoScroll){
                        var scrollTo = $('#datatable');
                        if ($(scrollTo).length > 0){
                            $('html, body').stop().animate({scrollTop: $(scrollTo).offset().top}, '1000', 'linear');
                        }
                    }

                    // if (jsonData.total == 1) {
                    //     $('a.data-modal').click();
                    // }

                }
            }

            /*Initial Datatable Build*/
            table = $(divTable).DataTable(tableSettings);
        }

        if (urlCheck) {
            $.jsonp({
                type: "GET",
                url: url,
                cache: false,
                callbackParameter: "callback",

                success: function(json) {
                    loadData(json);
                },
                error: function(xhr, textStatus, errorThrown) {
                    $('.error-message').text('We are unable to complete your request at this time.').removeClass('hidden');
                    loadBlankTable(url, target);
                },
                complete: function(xOptions, textStatus) {
                    $body.removeClass("loading");
                    $('body form.ws-validate').find(':input[type=submit]').prop('disabled', false);
                },
                beforeSend: function(xOptions) {
                    $body.addClass("loading");
                }
            });
        }

        else {
            loadData(url);
        }


    } else {
        loadBlankTable(url, target);
    }
}

var loadBlankTable = function(url, target){

    table = $(divTable).DataTable({

        lengthMenu: [
            [0],
            [0]
        ],
        searching: false,
        paging: false,
        info: false,
        order: [],
    });

    if (typeof onTableLoad === 'function'){
        setTimeout(function(){
            onTableLoad(url, target);
        }, 500);
    }
}

var removeDuplicates = function(data, key){
    //Setup Object
    var tmp = {};
    var update = [];
    //Loop through data and save the first captured rows.
   $.each(data, function(index, value) {
        var uid = value[key];
        if(!(uid in tmp)){
            tmp[uid] = '';
            update.push(value);
        }
    });
    
    return update;
}

var formatBytes = function (bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

var formatMoney = function (n) {
    n = Number(n);
    return "$" + (Math.round(n * 100) / 100).toLocaleString();
}