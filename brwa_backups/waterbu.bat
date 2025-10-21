@echo off
REM Activate ArcGIS Pro Python environment and run the script

REM Set path to ArcGIS Pro Python interpreter
set PYTHON_EXE="C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"

REM Set path to your Python script
set SCRIPT_PATH="S:\BU_Databases\scripts\scheduled_tasks\script_water\waterbu-logging.py"

REM Run the script
%PYTHON_EXE% %SCRIPT_PATH%