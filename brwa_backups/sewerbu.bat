@echo off
REM Activate ArcGIS Pro Python environment and run the script

REM Set path to ArcGIS Pro Python interpreter
set PYTHON_EXE="C:\Users\jhayes\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone-20250207\python.exe"

REM Set path to your Python script
set SCRIPT_PATH="S:\BU_Databases\scripts\scheduled_tasks\script_sewer\sewerbu-logging.py"

REM Run the script
%PYTHON_EXE% %SCRIPT_PATH%

