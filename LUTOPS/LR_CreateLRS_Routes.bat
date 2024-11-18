::Create_LRS_Routes.bat
::Builds automated linear referencing routes
::
REM @ECHO OFF

start/wait "" "D:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\LR01_DownloadStr.py"

start/wait "" "D:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\LR_TimeDelay.py"

start/wait "" "D:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\LR02_CreateLIDRoutes.py"

start/wait "" "D:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\LR_TimeDelay.py"

start/wait "" "D:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\LR03_CreateCalibPoints.py"

start/wait "" "D:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\LR_TimeDelay.py"

start/wait "" "D:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\LR04_CreateLRSRoutes.py"

start/wait "" "D:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\LR_TimeDelay.py"

start/wait "" "D:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\LR05_DeleteLoops.py"

start/wait "" "D:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\LR_TimeDelay.py"

start/wait "" "D:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\LR06_AddLoops.py"


