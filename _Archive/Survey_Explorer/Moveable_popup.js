// code to enable movable popups in web appbuilder
// this worked for me using the 2.25 dev edition
// must reaplce css and js code


// replace all common.css with this code
// location - [app instal]\server\apps\[app#]\themes\LaunchpadTheme\common.css
@import url("panels/LaunchpadPanel/style.css");


.esriPopupWrapper .title {
    cursor: move;
}
.esriPopup .hidden {
    display: none !important;
}

@import url("panels/DockablePanel/style.css"); 
/********** styles for simple panel***********/
.jimu-simple-panel{
  -moz-border-radius: 4px;
  -webkit-border-radius: 4px;
  border-radius: 4px;
/* }
 .jimu-subtitle{ - this stays commented out as part of default config.
  opacity: 0.5; */
} 
.jimu-link{
  opacity: 0.8;
}


// replace all the mo.createWebMap with this code.
// location - [app instal]\server\apps\[app#]\jimu.js\utils.js

// added - define(['dojo/dnd/Moveable', 'dojo/dom-class'], 
// added - function(Moveable, domClass)
define([
  'dojo/_base/lang',
  'dojo/_base/array',
  'dojo/_base/html',
  'dojo/_base/sniff',
  'dojo/_base/config',
  'dojo/dnd/Moveable',
  'dojo/io-query',
  'dojo/query',
  'dojo/NodeList-traverse',
  'dojo/Deferred',
  'dojo/promise/all',
  'dojo/on',
  'dojo/dom-class',
  'dojo/json',
  'dojo/cookie',
  'dojo/number',
  'dojo/date/locale',
  'dojo/i18n!dojo/cldr/nls/number',
  'dojox/encoding/base64',
  'esri/lang',
  'moment/moment',
  'esri/arcgis/utils',
  'esri/dijit/PopupTemplate',
  'esri/SpatialReference',
  'esri/geometry/Extent',
  'esri/geometry/geometryEngine',
  'esri/geometry/Multipoint',
  'esri/geometry/Polyline',
  'esri/geometry/Polygon',
  'esri/geometry/webMercatorUtils',
  'esri/tasks/GeometryService',
  'esri/tasks/ProjectParameters',
  'esri/tasks/FeatureSet',
  'esri/symbols/PictureMarkerSymbol',
  'esri/urlUtils',
  'esri/request',
  'esri/tasks/query',
  'esri/tasks/QueryTask',
  'esri/graphicsUtils',
  'jimu/portalUrlUtils',
  './shared/utils',
  './accessibleUtils',
  './zoomToUtils',
  'libs/caja-html-sanitizer-minified'
],

function(lang, array, html, has, config, Moveable, ioQuery, query, nlt, Deferred, all, on, domClass, json, cookie,
dojoNumber, dateLocale, nlsBundle, base64, esriLang, moment, arcgisUtils, PopupTemplate, SpatialReference,
Extent, geometryEngine, Multipoint, Polyline, Polygon, webMercatorUtils, GeometryService, ProjectParameters,
FeatureSet, PictureMarkerSymbol, esriUrlUtils, esriRequest, EsriQuery, QueryTask, graphicsUtils,
portalUrlUtils, sharedUtils, accessibleUtils, zoomToUtils
) { 
  
//-----------------------------------------------------------------------------------------------

// replace all the mo.createwebmap code with below
// aprox line 1201
mo.createWebMap = function(portalUrl, itemId, mapDiv, /* optional */ options) {
  //var arcgisUrlOld = arcgisUtils.arcgisUrl;
  portalUrl = portalUrlUtils.getStandardPortalUrl(portalUrl);
  var itemUrl = portalUrlUtils.getBaseItemUrl(portalUrl);
  arcgisUtils.arcgisUrl = itemUrl;
  var def = arcgisUtils.createMap(itemId, mapDiv, options);
  def.then(function (response){
    var map = response.map;
    var handle = query(".title", map.infoWindow.domNode)[0];
    var dnd = new Moveable(map.infoWindow.domNode, {
        handle: handle
    });

    // when the infoWindow is moved, hide the arrow:
    on(dnd, 'FirstMove', function() {
      // hide pointer and outerpointer (used depending on where the pointer is shown)
      var arrowNode =  query(".outerPointer", map.infoWindow.domNode)[0];
      domClass.add(arrowNode, "hidden");
      
      var arrowNode =  query(".pointer", map.infoWindow.domNode)[0];
      domClass.add(arrowNode, "hidden");
  }.bind(this));
  });
  return def;
};
