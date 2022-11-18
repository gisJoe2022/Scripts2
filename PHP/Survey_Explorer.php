<?php
    /*iSpirits Queries*/
    require '../../config/global.php';
    require '../../config/servers.php';
    $server_address = $imssqlsurvey_address;
    $database_info = $imssqlsurvey_info;
    require '../../config/api.php';
    // Grab Records
    WashCoAPI::Serve('GET', '/(#any)/', function ($table)
    {
        $conn = WashCoAPI::Connect($GLOBALS['server_address'], $GLOBALS['database_info']);
        /*Grab and sanitize url param values*/
        function URLParamstoQuery($data, $addAnd = null) {
            //Setup Object
            $updatedData = '';
            //Loop through data and save the first captured rows.
            foreach ($data as $key => $value) {
                $pvalue = isset($_GET[$key]) ? urldecode($_GET[$key]) : '';
                // Sanitize input
                $pvalue = preg_replace('/[^A-Za-z0-9-,.\/\ ]/', '', $pvalue);
                // Add AND if multiple params or requested
                $and = ($updatedData || $addAnd) ? " AND " : " ";
                // Query Builder
                $updatedData .= ($pvalue) ? $and . str_replace("pvalue",$pvalue,$value) : '';
            }
            return $updatedData;
        }
        // Multiple Surveys
        if ($table === "search"){
            /*Grab Search By*/
            $searchby = isset($_GET['searchby']) ? urldecode($_GET['searchby']) : '';
            if ($searchby == "search-survey"){
                /*Grab URL Params*/
                $urlParams = URLParamstoQuery(
                    array(
                        "surveynumber" => "Survey_Main.surveynumber IN (pvalue)",
                        "surveyornumber" => "Surveyors.surveyornumber LIKE '%pvalue%'",
                        "iclient" => "Survey_Main.client LIKE 'pvalue'",
                        "fileddatemin" => "Survey_Main.Filed >= Convert(datetime, 'pvalue' )",
                        "fileddatemax" => "Survey_Main.Filed <= Convert(datetime, 'pvalue' )",
                        "tr" => "Survey_TRS.TR='pvalue'",
                        "sec" => "Survey_TRS.SEC='pvalue'",
                        "qtr" => "Survey_TRS.QTR ='pvalue'",
                        "surveyorname" => "Surveyors.surveyorname LIKE '%pvalue%'",
                        "businessname" => "Survey_Main.WASHCO_COMPANYNAME LIKE 'pvalue'",
                        "receiveddatemin" => "Survey_Main.Date_Survey >= Convert(datetime, 'pvalue' )",
                        "receiveddatemax" => "Survey_Main.Date_Survey <= Convert(datetime, 'pvalue' )",
                    ), true
                );
                $reports = WashCoAPI::Run($conn, "SELECT TOP 700 Survey_Main.Surveynumber, Survey_Main.Date_Survey, Surveyors.surveyornumber, Survey_Main.Client, Survey_Main.Filed, Surveyors.Surveyorname, Surveyors.surveyornumber, Survey_Main.WASHCO_COMPANYNAME, Survey_TRS.TRSQTR
                FROM Survey_Main, Surveyors,Survey_TRS
                WHERE Survey_Main.surveyornumber=Surveyors.surveyornumber AND Survey_Main.surveynumber=Survey_TRS.surveynumber AND Survey_Main.Canceled=0 $urlParams
                ORDER BY Survey_Main.surveynumber",NULL,2);
                // Group Town/Section/Range
                $reports = groupFields($reports, 'Surveynumber', array('TRSQTR'));
            }
            else if ($searchby == "search-benchmark"){
                /*Grab URL Params*/
                $urlParams = URLParamstoQuery(
                    array(
                        // append 'W' to end of pvalue for tr
                        "benchmarkid" => "Benchmarks.ID IN (pvalue)",
                        "tr" => "Benchmarks.T_R='pvalueW'",
                        "sec" => "Benchmarks.Section='pvalue'",
                        "qtr" => "Benchmarks.QTRSEC ='pvalue'",
                    )
                );
                $reports = WashCoAPI::Run($conn, "SELECT DISTINCT TOP 700 Benchmarks.ID,'http://mtbachelor.co.washington.or.us/images/survey/BM/BM_Photos/bm' + CAST(Benchmarks.ID As VARCHAR(8)) + '.pdf' AS BmPhoto,bmSitePhoto.bm_site_photo,Benchmarks.STAMPING, Benchmarks.T_R AS TR,Benchmarks.SECTION as Sec,Benchmarks.QTRSEC as QTR, Benchmarks.ELEVATION1
                FROM Benchmarks LEFT JOIN bmSitePhoto ON Benchmarks.ID = bmSitePhoto.ID
                WHERE $urlParams
                ORDER BY Benchmarks.ID",NULL,2);
            }
            else if ($searchby == "search-corner"){
                /*Grab URL Params*/
                /*Required Transformation of param values*/
                $tr = isset($_GET['tr']) ? urldecode($_GET['tr']) : '';
                /*Sanitize Input*/
                $tr = preg_replace('/[^A-Za-z0-9]/', '', $tr);
                $twn = ($tr) ? '0' . $tr[0] : '';
                $twndir  = ($tr) ? $tr[1] : '';
                $rng = ($tr) ? '0' . $tr[2] : '';
                $urlParams = URLParamstoQuery(
                    array(
                        "cornerid" => "corner_search19.CORNERID IN ('pvalue')",
                        "surveyorname" => "corner_search19.STATUSSURVEYOR LIKE 'pvalue'",
                        "surveyornumber" => "corner_search19.surveyornumber LIKE 'pvalue'",
                        "tr" => "Corner_TRS.TWN LIKE '" . $twn . "' AND Corner_TRS.TWNDIR LIKE '" . $twndir . "' AND Corner_TRS.RNG LIKE '" . $rng . "' AND corner_search19.CORNERID=Corner_TRS.CORNERID",
                        "sec" => "Corner_TRS.SECTION LIKE 'pvalue'",
                        "qtr" => "Corner_TRS.SECTIONDIR LIKE 'pvalue'",
                        "bookpage" => "corner_search19.Book_Page_Entry LIKE 'pvalue%'",
                    )
                );
                $reports = WashCoAPI::Run($conn, "SELECT DISTINCT TOP 700 corner_search19.CORNERID,'http://mtbachelor.co.washington.or.us/images/survey/BTBOOKS/SitePhoto/' + corner_search19.CORNERID + '.pdf' AS sitePhoto,corner_search19.BOOK_PAGE_ENTRY As BookPage,Corner_Photo.Photo_name,corner_search19.GPS_ID,corner_search19.DESCRIPTION
                FROM corner_search19 LEFT JOIN Corner_Photo ON corner_search19.CORNERID = Corner_Photo.CornerID,Corner_TRS
                WHERE $urlParams
                ORDER BY corner_search19.CORNERID",NULL,2);
                // Group by CORNERID
                $reports = groupFields($reports, 'CORNERID', array('BookPage','DESCRIPTION'));
            }
            else if ($searchby == "search-geocontrol"){
                /*Grab URL Params*/
                $urlParams = URLParamstoQuery(
                    array(
                        "controlname" => "Geocontrol_Main.Fullname LIKE 'pvalue%'",
                        "surveyorname" => "surveyors.surveyorname LIKE '%pvalue%' AND (Surveyors.Surveyornumber=Geocontrol_Main.Surveyornumber)",
                        "tr" => "Geocontrol_TRS.T_R='pvalue'",
                        "sec" => "Geocontrol_TRS.Section='pvalue'",
                        "qtr" => "Geocontrol_TRS.[1/4] ='pvalue'",
                    )
                );
                /*Required Transformation of param values*/
                $tr = isset($_GET['tr']) ? urldecode($_GET['tr']) : '';
                $sec = isset($_GET['sec']) ? urldecode($_GET['sec']) : '';
                $qtr = isset($_GET['qtr']) ? urldecode($_GET['qtr']) : '';
                $trs = ($tr || $sec || $qtr) ? ' AND Geocontrol_Main.Fullname=Geocontrol_TRS.Fullname' : '';
                $reports = WashCoAPI::Run($conn, "SELECT DISTINCT TOP 700 Geocontrol_Main.Fullname,Geocontrol_Main.Name,Geocontrol_Main.Latitude,Geocontrol_Main.Longitude,Geocontrol_Main.DESCRIPTION
                FROM Geocontrol_Main,Surveyors,Geocontrol_TRS
                WHERE $urlParams $trs
                ORDER BY Geocontrol_Main.Fullname",NULL,2);
            }
            else if ($searchby == "search-plat"){
                /*Grab URL Params*/
                $urlParams = URLParamstoQuery(
                    array(
                        "platname" => "Plat_main.PlatName LIKE 'pvalue%'",
                        "bookpage" => "Plat_main.[Book/Page] LIKE '%pvalue%'",
                        "docnumber" => "Plat_main.DocNumber LIKE '%pvalue%'",
                        "surveyorname" => "surveyors.surveyorname LIKE '%pvalue%'",
                        "surveyornumber" => "surveyors.surveyornumber LIKE '%pvalue%'",
                        "businessname" => "Plat_Main.businessname LIKE '%pvalue%'",
                        "tr" => "Plat_TRS.[T-R]='pvalue'",
                        "sec" => "Plat_TRS.Sec='pvalue'",
                        "qtr" => "Plat_TRS.QTR='pvalue'",
                        "city" => "CityCode.CityName LIKE '%pvalue%'",
                        "declarant" => "Plat_main.Declarant LIKE 'pvalue%'",
                        "recordeddatemin" => "Plat_Main.Recorded >= Convert(datetime, 'pvalue' )",
                        "recordeddatemax" => "Plat_Main.Recorded <= Convert(datetime, 'pvalue' )",
                        "receiveddatemin" => "Plat_Main.Received >= Convert(datetime, 'pvalue' )",
                        "receiveddatemax" => "Plat_Main.Received <= Convert(datetime, 'pvalue' )",
                    ), true
                );
                $reports = WashCoAPI::Run($conn, "SELECT DISTINCT TOP 700 Plat_Main.Platname, Plat_Main.BusinessName,Plat_Main.Surveyornumber,Plat_Main.DocNumber, Plat_Main.[Book/Page] AS BookPage, Plat_Main.Recorded,Plat_Main.Received,CityCode.CityName,Plat_Main.Declarant, Surveyors.SurveyorName
                FROM Plat_Main, Surveyors, Plat_TRS,CityCode
                WHERE (Plat_TRS.PlatName= Plat_Main.PlatName) AND (Surveyors.Surveyornumber=Plat_Main.Surveyornumber) AND (Plat_Main.City = CityCode.CityCode) AND (Plat_Main.Canceled=0) $urlParams
                ORDER BY (Plat_Main.platname)",NULL,2);
            }
            else if ($searchby == "search-taxmap"){
                /*Grab URL Params*/
                $urlParams = URLParamstoQuery(
                    array(
                        "tlid" => "tlid LIKE 'pvalue%'",
                        "sitestrno" => "HOUSE_NUMBER = pvalue",
                    )
                );
                $reports = WashCoAPI::Run($conn, "SELECT TOP 700 tlid, OwnerName, OwnerAddr, OwnerAddr2, OwnerAddr3, OwnerCity, OwnerState, OwnerZip, HOUSE_NUMBER, Fulladdress, CITY, LandVal, BldgVal, TotalVal, BldgSqft, Acres, YearBuilt, SaleDate, SalePrice, Account, X_Coordinate, Y_Coordinate
                FROM washgeo
                WHERE $urlParams
                ORDER BY tlid ASC",NULL,2);
                /*Remover Owner information for non-county network requests*/
                if (!isCountyNetwork()){
                    $reports = removeFields($reports, ['OwnerName', 'OwnerAddr', 'OwnerAddr2', 'OwnerAddr3', 'OwnerCity', 'OwnerState', 'OwnerZip']);
                }
            }
            else if ($searchby == "search-countyroad"){
                /*Grab URL Params*/
                $urlParams = URLParamstoQuery(
                    array(
                        "cntyroadid" => "CROAD_ID LIKE 'pvalue%'",
                    )
                );
                $reports = WashCoAPI::Run($conn, "SELECT DISTINCT TOP 700 CROAD_ID,Date,COMMENTS,COMMENTS2
                FROM CntyRoad_Main
                WHERE $urlParams
                ORDER BY CROAD_ID ASC",NULL,2);    
            }
            else if ($searchby == "search-smaps"){
                // Simply checks if application returns a 200 or 500 error.
                function get_http_response_code($theURL) {
                    $headers = get_headers($theURL);
                    return substr($headers[0], 9, 3);
                }
                $tr = isset($_GET['tr']) ? urldecode($_GET['tr']) : '';
                $sec = isset($_GET['sec']) ? urldecode($_GET['sec']) : '';
                // Sanitize Inputs
                $tr = preg_replace('/[^A-Za-z0-9 ]/', '', $tr);
                $sec = preg_replace('/[^A-Za-z0-9 ]/', '', $sec);
                // Transform data (Append 0 to single digits)
                $sec = sprintf("%02d", $sec);
                if ($tr){
                    $url = 'http://mtbachelor.co.washington.or.us/images/pdfbuilderasp/tiff2pdf.asp?doctype=section&imageto=' . $tr . 'w' . $sec;
                    $httpcode = get_http_response_code($url);
                    if ($httpcode === '200'){
                        $obj = array('url' => $url);
                        $reports = array(
                            $obj
                        );
                    }
                }  
            }
        }
        // Single Row Reports
        else if ($table === "id"){
            $type = isset($_GET['type']) ? urldecode($_GET['type']) : '';
            $uid = isset($_GET['uid']) ? urldecode($_GET['uid']) : '';
            $uid = preg_replace('/[^A-Za-z0-9-,\/\.() ]/', '', $uid);
            if ($uid && $type) {
                if ($type == "search-survey"){
                    $reports = WashCoAPI::Run($conn, "SELECT DISTINCT Survey_Image.filename,Survey_Main.Surveynumber, Survey_Main.Received,Survey_Main.Comments,Survey_Main.Date_Survey,Survey_TRS.TRSQTR,Surveyors.Surveyorname,Survey_Main.Client, Survey_Main.platbound,Survey_Main.pla,Survey_Main.WASHCO_COMPANYNAME, Surveyors.Surveyornumber,Survey_Main.Filed
                    FROM Survey_Main, Surveyors, Survey_TRS,Survey_Image
                    WHERE Survey_Main.surveynumber=Survey_Image.surveynumber AND Survey_Main.surveyornumber=Surveyors.surveyornumber AND Survey_Main.surveynumber=Survey_TRS.surveynumber AND Survey_Main.surveynumber IN ('$uid')
                    ORDER BY Survey_Main.surveynumber",NULL,24);
                    // Group Town/Section/Range
                    $reports = groupFields($reports, 'Surveynumber', array('TRSQTR', 'filename'));
                }
                else if ($type == "search-benchmark"){
                    $reports = WashCoAPI::Run($conn, "SELECT DISTINCT Benchmarks.ID,Benchmarks.STAMPING, Benchmarks.Tile_Name, Benchmarks.ELEVATION1, Benchmarks.monument,benchmarks.city,benchmarks.state,benchmarks.established_by, benchmarks.Date_established,benchmarks.location,benchmarks.ref1,benchmarks.ref2, benchmarks.ref3,benchmarks.ref4,benchmarks.ref5,benchmarks.ref6,benchmarks.checked_on2001,benchmarks.checked_by2001, 'http://mtbachelor.co.washington.or.us/images/survey/BM/BM_Photos/bm' + CAST(Benchmarks.ID As VARCHAR(8)) + '.pdf' AS BmPhoto,bmSitePhoto.bm_site_photo, benchmarks.condition2001,benchmarks.cornerid,benchmarks.gcname,benchmarks.county
                    FROM Benchmarks LEFT JOIN bmSitePhoto ON Benchmarks.ID = bmSitePhoto.ID
                    WHERE Benchmarks.ID IN ('$uid')
                    ORDER BY Benchmarks.ID",NULL,24);
                }
                else if ($type == "search-corner"){
                    $reports = WashCoAPI::Run($conn, "SELECT DISTINCT v_Corner_Main_all.CORNERID,v_Corner_Main_all.BOOK_PAGE_ENTRY, v_Corner_Main_all.DESCRIPTION,v_Corner_Main_all.STATUSDATE,v_Corner_Main_all.SURVEYORNUMBER, Surveyors.Surveyorname,v_Corner_Main_all.BLMNO,Corner_Image.filename,'http://mtbachelor.co.washington.or.us/images/survey/BTBOOKS/SitePhoto/' + v_Corner_Main_all.CORNERID + '.pdf' AS sitePhoto,Corner_Photo.Photo_name
                    FROM v_Corner_Main_all LEFT JOIN Corner_Photo ON v_Corner_Main_all.CORNERID = Corner_Photo.CornerID,Surveyors,Corner_Image
                    WHERE v_Corner_Main_all.Surveyornumber=surveyors.surveyornumber AND v_Corner_Main_all.CORNERID=Corner_Image.CORNERID AND v_Corner_Main_all.CORNERID IN ('$uid')
                    ORDER BY v_Corner_Main_all.CORNERID",NULL,24);
                    // Group by CORNERID
                    $reports = groupFields($reports, 'CORNERID', array('BOOK_PAGE_ENTRY','DESCRIPTION', 'filename', 'SURVEYORNUMBER', 'Surveyorname', 'STATUSDATE'));
                }
                else if ($type == "search-geocontrol"){
                    $reports = WashCoAPI::Run($conn, "SELECT DISTINCT Geocontrol_Main.Fullname,Geocontrol_Main.Name,Geocontrol_Main.Latitude, Geocontrol_Main.Longitude,Geocontrol_Main.DESCRIPTION,Geocontrol_Main.[station number] as stationnumber, Geocontrol_Main.northfeet,Geocontrol_Main.eastfeet,Geocontrol_Main.northmeter,Geocontrol_Main.eastmeter, Geocontrol_Main.grid_scale,Geocontrol_Main.convergenc,Geocontrol_Main.combined_f,Geocontrol_Main.ellipsoid, Geocontrol_Main.govcorn,Geocontrol_Main.method,Geocontrol_Main.projection,Geocontrol_Main.corner_id, Geocontrol_Main.surveyornumber,Geocontrol_Main.[accepted?] as accepted,Geocontrol_Main.condition,surveyors.surveyorname, Geocontrol_TRS.T_R as TR,Geocontrol_TRS.Section as Sec,Geocontrol_TRS.[1/4] as QTR,Geocontrol_Image.filename
                    FROM Geocontrol_Main,Geocontrol_TRS,surveyors,Geocontrol_Image
                    WHERE Geocontrol_Main.Fullname=Geocontrol_TRS.Fullname AND Geocontrol_Main.surveyornumber =surveyors.surveyornumber AND Geocontrol_Image.fullname=Geocontrol_Main.fullname AND Geocontrol_Main.fullname IN ('$uid') 
                    ORDER BY Geocontrol_Main.Fullname",NULL,24);
                    // Group by filename
                    $reports = groupFields($reports, 'Fullname', array('filename'));
                }
                else if ($type == "search-plat"){
                    $reports = WashCoAPI::Run($conn, "SELECT DISTINCT Plat_Main.Platname, Plat_Main.Surveyornumber, Plat_Main.DocNumber, Plat_Main.[Book/Page] AS BOOKPAGE, Plat_Main.Recorded,CityCode.CityName, Surveyors.SurveyorName,Plat_TRS.[T-R] AS TR, Plat_TRS.Sec, Plat_TRS.[QTR] AS QTR, Plat_Main.Declarant,Plat_Main.Lots,Plat_Main.Tracts,Plat_Main.BusinessName,Plat_Main.Proj,Plat_Main.CaseFileNumber, Plat_Image.filename
                    FROM Plat_Main, Surveyors,Plat_TRS, Plat_Image,CityCode
                    WHERE (Surveyors.Surveyornumber=Plat_Main.Surveyornumber) AND (Plat_TRS.PlatName=Plat_Main.PlatName) AND (Plat_Main.City = CityCode.CityCode) AND (Plat_Main.PlatName=Plat_Image.platname) AND (Plat_main.PlatName IN ('$uid'))
                    ORDER BY Plat_Main.platname",NULL,24);
                    // Group Files
                    $reports = groupFields($reports, 'Platname', array('filename'));
                }
                else if ($type == "search-taxmap"){
                    $reports = WashCoAPI::Run($conn, "SELECT tlid, OwnerName, OwnerAddr, OwnerAddr2, OwnerAddr3, OwnerCity, OwnerState, OwnerZip, HOUSE_NUMBER, Fulladdress, CITY, LandVal, BldgVal, TotalVal, BldgSqft, Acres, YearBuilt, SaleDate, SalePrice, Account, X_Coordinate, Y_Coordinate
                    FROM washgeo
                    WHERE tlid IN ('$uid')
                    ORDER BY tlid ASC",NULL,24);
                    // Grab Taxmap Documents
                    // Prepare groupname variable
                    $groupname = substr($uid, 0, 7);
                    $SECTNUM1 = substr($uid, 3, 2);
                    $SECTNUM2 = substr($uid, 5, 2);
                    $SECTNUM3 = substr($uid, 3, 4);
                    $SECTNUM4 = substr($uid, 5, 1);
                    $SECTNUM5 = substr($uid, 6, 1);
                    if ($SECTNUM1 == "00"){
                        if ($SECTNUM3 == "0000") {
                            $groupname = substr($uid, 0, 3);
                        }
                        if ($SECTNUM3 != "0") {
                            $groupname = substr($uid, 0, 3) . $SECTNUM4;
                        } 
                    }
                    if ($SECTNUM2 == "00"){
                        $groupname = substr($uid, 0, 5);
                    }
                    if ($SECTNUM5 == "0"){
                        $groupname = substr($uid, 0, 6);
                    }
                    $conn2 = WashCoAPI::Connect($GLOBALS['vsqlapp_gis_address'], $GLOBALS['vsqlapp_gis_info']);
                    $taxmap = WashCoAPI::Run($conn2, "EXEC usp_GetTaxmaps @groupname = ?, @wherecriteria = ?", array( $groupname, '1' ), 24);
                    $reports[0]['filename'] = $taxmap;
                    // Remover Owner information for non-county network requests
                    if (!isCountyNetwork()){
                        $reports = removeFields($reports, ['OwnerName', 'OwnerAddr', 'OwnerAddr2', 'OwnerAddr3', 'OwnerCity', 'OwnerState', 'OwnerZip']);
                    }
                }
                else if ($type == "search-countyroad"){
                    $reports = WashCoAPI::Run($conn, "SELECT DISTINCT CntyRoad_Main.CROAD_ID,CntyRoad_Main.Date,CntyRoad_Main.COMMENTS,CntyRoad_Main.COMMENTS2,CntyRoad_Image.filename
                    FROM CntyRoad_Main, CntyRoad_Image
                    WHERE CntyRoad_Main.CROAD_ID LIKE '$uid' AND CntyRoad_Image.CROAD_ID LIKE '$uid'
                    ORDER BY CntyRoad_Main.CROAD_ID ASC",NULL,24);
                    // Group Files
                    $reports = groupFields($reports, 'CROAD_ID', array('filename'));
                }
            }
        }
        // Surveyor Name and Business Input Data
        else if ($table === "input"){
            /*Reports*/
            $reports = array();
            $surveyorname = '';
            $businessname = '';
            if(isCountyNetwork()){
                $surveyorname = WashCoAPI::Run($conn, "SELECT SurveyorName
                    FROM dbo.Surveyors
                    Order By surveyorname",NULL,48);
                $surveyorname = removeEmpty($surveyorname, 'SurveyorName');
                $surveyorname = groupObjects($surveyorname, 'SurveyorName');
            }
            $businessname = WashCoAPI::Run($conn, "SELECT WashCo_CompanyName
                FROM COMPANY
                Order By washco_companyname",NULL,48);
            $businessname = groupObjects($businessname, 'WashCo_CompanyName');
            if ($surveyorname){
                $reports['surveyorname'] = $surveyorname;
            }
            if ($businessname){
                $reports['businessname'] = $businessname;
            }
        }
        // Custom Reports/Views
        else if ($table === "report"){
            $searchby = isset($_GET['searchby']) ? urldecode($_GET['searchby']) : '';
            if ($searchby) {
                if ($searchby == "plat-query"){
                    $reports = WashCoAPI::Run($conn, "EXEC ProjectReviews", NULL, 24);
                }
                else if ($searchby == "plat-name"){
                    $reports = WashCoAPI::Run($conn, "EXEC usp_PlatNameReport", NULL, 24);
                }
                else if ($searchby == "street-name"){
                    $reports = WashCoAPI::Run($conn, "SELECT UPPER(road_names.NAME) AS NAME, road_names.LOCATION, road_names.q_SECTION, road_names.CITY, case PRIVATE when 0 then '' when 1 then 'PRIVATE' end PRIVATE, road_names.NOTES
                        FROM road_names
                        ORDER BY NAME ASC",NULL,48);
                }
            }
        }
        $result = $reports ? $reports : WashCoAPI::$HTTP[204];
        return WashCoAPI::Reply($result);
    });
    exit(WashCoAPI::Reply(WashCoAPI::$HTTP[400]));
?>