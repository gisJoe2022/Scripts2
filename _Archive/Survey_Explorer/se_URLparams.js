require([
    // "esri/map", 
    "esri/arcgis/utils",
    "esri/dijit/LayerList",
    "esri/dijit/Search",
    "esri/layers/FeatureLayer",
    "esri/InfoTemplate",
    "esri/symbols/SimpleMarkerSymbol", //
    "esri/InfoTemplate", // //f43b537eaca542dbb7881f020a6577bc
    // "esri/virtualearth/VETiledLayer",
    "dijit/layout/BorderContainer",
    "dijit/layout/ContentPane",
    "dojo/domReady!"
], function(
    //Map,   
    arcgisUtils,
    LayerList,
    // VETiledLayer,
    Search,
    SimpleMarkerSymbol,
    InfoTemplate
) {

    //Create a map based on an ArcGIS Online web map id also: code below was... createMap("c266db2518114177a1390adb70c6a716" ...
    var esriLogoOff = {
            logo: false
        }
        //webmap from copy of survey explorer2 (AGOL:Survey Explorer - map) was use "a6c4c1ef644e4d719a656a65dc1682b6" below
    arcgisUtils.createMap("a6c4c1ef644e4d719a656a65dc1682b6", "map", {
        mapOptions: esriLogoOff
    }).then(function(response) {
        //webmap was on ActiveG~  
        //arcgisUtils.createMap("f43b537eaca542dbb7881f020a6577bc", "map", {mapOptions: esriLogoOff}).then(function(response){  
        //arcgisUtils.createMap("657b7f0d16434813a0f576e2a2b9177e", "map", {mapOptions: esriLogoOff}).then(function(response){
        var myWidget = new LayerList({
            map: response.map,
            layers: arcgisUtils.getLayerList(response)
        }, "layerList");
        myWidget.startup();

        //add Bing Maps
        // var veTileLayer = new VETiledLayer({
        //  bingMapsKey:"AuXx8iHX50DkhH1VCkDHCfKg84WONr2R-ip0KPPOSL626LvY-ntuGvJeX1fpmDjp",
        // mapStyle: VETiledLayer.MAP_STYLE_AERIAL});
        // map.addLayer(veTileLayer);

        // search.source.indexOf(1).placeholder="3771",

        var s = new Search({
            enableLabel: true,
            addLayersFromMap: true,
            enableHighlight: true,
            enableSuggestions: true,
            maxSuggestions: 30,
            showSuggestions: true,
            enableHighlight: true,
            //enableSuggestionsMenu: true,
            highlightGraphic: true,
            //highlightSymbol: true,
            map: response.map,
            sources: []
        }, "search");



        //listen for the load event and set the source properties 
        //        search.on("load", function () {

        //            var sources = search.sources;
        //           sources.push({
        //              featureLayer: layer,
        //               placeholder: "Spain",
        //               enableLabel: true,
        //            searchFields: ["Country"],
        //            displayField: "Country",
        //           exactMatch: false,
        //           outFields: ["*"],

        //Create an InfoTemplate and include three fields
        //           infoTemplate: new InfoTemplate("Ecological Footprint", "<a href= ${URL} target=_blank ;'>Additional Info</a></br></br>Country: ${Country}</br>Rating: ${Rating}")

        //       });


        // })
        

        s.on('load', function(e) {

            var urlParams = getAllUrlParams();

            if (urlParams['type'] && urlParams['id']) {

                // Grab all search groups.
                var searchGroups = $('div.searchMenu.sourcesMenu ul[role=menu]').children('li');

                // Itterate through search groups and match text.
                var groupFound = 0;
                $.each(searchGroups, function() {
                    if (urlParams['type'].toLowerCase() == $(this)[0].innerHTML.toLowerCase()){
                        $(this).click();
                        groupFound = 1;
                        return false;
                    }
                });

                if (!groupFound){
                    $('div.searchMenu.sourcesMenu ul[role=menu]').children('li[data-index=all]').click();
                }

                console.log('set');
                s.set("value", decodeURIComponent(urlParams['id']));
                console.log('search');
                s.search().then(function(response) {
                    console.log(response.results);
                });
            }
        });

        s.on("suggest-results", function (e) {
            console.log ('suggest results', e);

        });

        s.startup();

    });

    $("#ui-settings-button").click(function() {
        $("#floatpanel").toggle(); //css("display", "inline")
    });

    $("#btnClose").click(function() {
        $("#floatpanel").toggle(); //close it for mibile
    });

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

    /*
    $("#map").click(function (){
    $("#floatpanel").hide(); //close floatpanel for mobile
    });
*/
});