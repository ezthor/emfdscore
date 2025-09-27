@echo off
REM Quick analysis script for Windows
REM This script activates the conda environment and runs the analysis

echo Activating eMFDscore environment...
call conda activate emfd
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Could not activate 'emfd' environment.
    echo Please run start_windows.bat first to set up the environment.
    pause
    exit /b 1
)

echo.
echo ================================
echo eMFDscore Analysis
echo ================================

REM Check if argument provided
if "%~1"=="" (
    echo Usage: run_analysis.bat [input_file] [options...]
    echo.
    echo Examples:
    echo   run_analysis.bat input.txt
    echo   run_analysis.bat document.pdf --show-summary
    echo   run_analysis.bat input.txt --dict-type mfd --output results.json
    echo.
    echo Running demo instead...
    python start.py
) else (
    echo Analyzing: %1
    python bin\moral_analyzer %*
)

echo.
echo Analysis complete!
pause