@echo off
REM Activate ArcGIS Pro Python environment and run the script

REM Set path to ArcGIS Pro Python interpreter
set PYTHON_EXE="C:\Users\jhayes\AppData\Local\miniconda3\python.exe"

REM Set path to your Python script
set SCRIPT_PATH="S:\Projects\2025_Projects\202517_Latency_Testing\latency.py"

REM Run the script
%PYTHON_EXE% %SCRIPT_PATH%
