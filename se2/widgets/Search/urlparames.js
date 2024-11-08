
// <!-- Add this line to new version of survey explorer -->
getAllUrlParams: function() {

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
},

      postCreate: function() {

        if (this.closeable || !this.isOnScreen) {
          html.addClass(this.searchNode, 'default-width-for-openAtStart');
        }

        this.listenWidgetIds.push('framework');
        this._pointOfSpecifiedUtmCache = {};
      },

      startup: function() {
        this.inherited(arguments);

        if (!(this.config && this.config.sources)) {
          this.config.sources = [];
        }

        coordinateFormatter.load();
        LayerInfos.getInstance(this.map, this.map.itemInfo)
          .then(lang.hitch(this, function(layerInfosObj) {
            this.layerInfosObj = layerInfosObj;
            this.own(this.layerInfosObj.on(
            'layerInfosFilterChanged',
            lang.hitch(this, this.onLayerInfosFilterChanged)));

            utils.setMap(this.map);
            utils.setLayerInfosObj(this.layerInfosObj);
            utils.setAppConfig(this.appConfig);
            when(utils.getConfigInfo(this.config)).then(lang.hitch(this, function(config) {
              return all(this._convertConfig(config)).then(function(searchSouces) {
                return array.filter(searchSouces, function(source) {
                  return source;
                });
              });
            })).then(lang.hitch(this, function(searchSouces) {
              if (!this.domNode) {
                return;
              }

              this.searchDijit = new Search({
                activeSourceIndex: searchSouces.length === 1 ? 0 : 'all',
                allPlaceholder: jimuUtils.stripHTML(esriLang.isDefined(this.config.allPlaceholder) ?
                  this.config.allPlaceholder : ""),
                autoSelect: true,
                enableButtonMode: false,
                enableLabel: false,
                enableHighlight: true,
                enableInfoWindow: true,
                showInfoWindowOnSelect: true,
                map: this.map,
                sources: searchSouces,
                //minCharacters: 1,
                theme: 'arcgisSearch'
              });
              html.place(this.searchDijit.domNode, this.searchNode);
              this.searchDijit.startup();

              this._resetSearchDijitStyle();

              this.own(
                this.searchDijit.watch(
                  'activeSourceIndex',
                  lang.hitch(this, '_onSourceIndexChange')
                )
              );

              this.own(
                on(this.searchDijit, 'search-results', lang.hitch(this, '_onSearchResults'))
              );

              this.own(
                on(this.searchDijit, 'suggest-results', lang.hitch(this, '_onSuggestResults'))
              );

              this.own(
                on(this.searchDijit, 'select-result', lang.hitch(this, '_onSelectResult'))
              );

              this.own(
                on(this.searchDijit, 'clear-search', lang.hitch(this, '_onClearSearch'))
              );

              this.own(
                aspect.around(this.searchDijit, '_search', lang.hitch(this, '_convertSR'))
              );

              this.own(
                aspect.before(this.searchDijit, '_formatResults',
                  lang.hitch(this.searchDijit, function(results, idx, value) {
                  try{
                    var newResults = array.map(results, function(result) {
                      if(result && (result instanceof Error || result.length >= 0)) {
                        return result;
                      } else {
                        return new Error( result && result.message || "Invalid query source or locator" );
                      }
                    });
                    return [newResults, idx, value];
                  } catch (err) {
                    console.log(err && err.message);
                    return [results, idx, value];
                  }
                }))
              );
              console.log('loaded Search');
              var data = this.getAllUrlParams();
              console.log(data);

              if (data['type'] && data['searchString']) {

                var searchGroups = $('div.searchMenu.sourcesMenu ul[role=menu]').children('li');
                console.log(searchGroups);

                var groupFound = 0;
                $.each(searchGroups, function() {
                    if (data['type'].toLowerCase() == $(this)[0].innerHTML.toLowerCase().replace(/\s/g, '')){
                        $(this).click();
                        groupFound = 1;
                        return false;
                    }
                });

                if (!groupFound){
                    $('div.searchMenu.sourcesMenu ul[role=menu]').children('li[data-index=all]').click();
                }

                this.searchDijit.set("value", decodeURIComponent(data['searchString']));
                this.searchDijit.search().then(function(response) {
                    console.log(response.results);
                });

              }
              // <!-- stops here - Add this line to new version of survey explorer -->

              /*****************************************
               * Binding events about 508 accessbility
               * ***************************************/

              if(searchSouces.length === 1){
                jimuUtils.initFirstFocusNode(this.domNode, this.searchDijit.inputNode);
              }else{
                jimuUtils.initFirstFocusNode(this.domNode, this.searchDijit.sourcesBtnNode);
              }
              jimuUtils.initLastFocusNode(this.domNode, this.searchDijit.submitNode);
              this.own(on(this.domNode, "keydown", lang.hitch(this, function(evt) {
                if(html.hasClass(evt.target, this.baseClass) && evt.keyCode === keys.ENTER) {//enter to first node
                  this.searchDijit.sourcesBtnNode.focus();
                }
                //esc to close searched list
                else if(!html.hasClass(evt.target, this.baseClass) && evt.keyCode === keys.ESCAPE) {
                  if(html.getStyle(this.searchResultsNode, 'display') === 'block'){
                    html.setStyle(this.searchResultsNode, 'display', 'none');
                  }
                }
              })));

              this.own(
                aspect.around(this.searchDijit, '_inputKey', lang.hitch(this, function(originalFun) {
                  return lang.hitch(this, function(e) {
                    var returnValue = null;
                    if(html.getStyle(this.searchResultsNode, 'display') === 'block') {
                      console.log("searchResultsNode");
                      this._inputKey(e);
                    } else {
                      returnValue = originalFun.apply(this.searchDijit, [e]);
                    }
                    return returnValue;
                  });
                }))
              );

              /*****************************************
               * Binding events for control result menu
               * ***************************************/
              this.own(
                on(this.searchDijit.domNode, 'click', lang.hitch(this, '_onSearchDijitClick'))
              );

              this.own(on(this.searchDijit.inputNode, "keyup", lang.hitch(this, function(e) {
                if (e.keyCode !== keys.ENTER && e.keyCode !== keys.UP_ARROW && e.keyCode !== keys.DOWN_ARROW) {
                  this._onClearSearch();
                }
              })));

              this.own(
                on(this.searchResultsNode, 'li:click', lang.hitch(this, '_onSelectSearchResult'))
              );
              this.own(
                on(this.searchResultsNode, 'li:keyup', lang.hitch(this, '_onSearchResultLiKey'))
              );

              this.own(on(
                this.searchResultsNode,
                '.show-all-results:click',
                lang.hitch(this, '_showResultMenu')
              ));

              this.own(
                on(window.document, 'click', lang.hitch(this, function(e) {
                  if (!html.isDescendant(e.target, this.searchResultsNode)) {
                    this._hideResultMenu();
                    this._resetSelectorPosition('.show-all-results');
                  }
                  if (!html.isDescendant(e.target, this.searchDijit.suggestionsNode)) {
                    this._hideSuggestionsMenu();
                  }
                }))
              );
              this.fetchData('framework');
            }));
          }));
      },