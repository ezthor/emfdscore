@echo off
REM Enhanced eMFDscore Windows Startup Script
REM This script activates conda environment and runs the moral framework analysis

echo ================================
echo Enhanced eMFDscore Windows Setup
echo ================================

REM Check if conda is available
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Conda is not found in PATH. Please install Anaconda/Miniconda and add it to PATH.
    echo Visit: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

REM Set environment name
set ENV_NAME=emfd

echo.
echo [1/4] Creating conda environment '%ENV_NAME%'...
call conda create -n %ENV_NAME% python=3.11 -y
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Environment might already exist or creation failed.
)

echo.
echo [2/4] Activating conda environment...
call conda activate %ENV_NAME%
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate environment '%ENV_NAME%'
    pause
    exit /b 1
)

echo.
echo [3/4] Installing dependencies...
pip install pandas progressbar2 nltk numpy spacy scikit-learn pdfplumber PyPDF2
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [4/4] Installing eMFDscore package...
pip install -e .
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install eMFDscore package
    pause
    exit /b 1
)

echo.
echo ================================
echo Installing spaCy English model
echo ================================

REM Try multiple methods to install spaCy model
echo Method 1: Direct download...
python -m spacy download en_core_web_sm
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: spaCy model installed successfully!
    goto :model_success
)

echo.
echo Method 1 failed. Trying Method 2: Manual download...
REM Create temporary directory for manual download
mkdir temp_model 2>nul
cd temp_model

echo Downloading spaCy model manually...
curl -L -o en_core_web_sm-3.8.0.tar.gz https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0.tar.gz
if %ERRORLEVEL% EQU 0 (
    echo Installing from downloaded file...
    pip install en_core_web_sm-3.8.0.tar.gz
    if %ERRORLEVEL% EQU 0 (
        cd ..
        rmdir /s /q temp_model
        echo SUCCESS: spaCy model installed via manual download!
        goto :model_success
    )
)

cd ..
rmdir /s /q temp_model 2>nul

echo.
echo Method 2 failed. Trying Method 3: Alternative installation...
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: spaCy model installed via alternative method!
    goto :model_success
)

echo.
echo WARNING: All spaCy model installation methods failed.
echo You may need to install it manually. See troubleshooting section below.
goto :model_failed

:model_success
echo.
echo ================================
echo Setup Complete!
echo ================================

echo Testing installation...
python -c "import emfdscore; print('✓ eMFDscore imported successfully')"
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✓ spaCy model loaded successfully')"

echo.
echo You can now use eMFDscore! Examples:
echo.
echo   # Analyze a text file:
echo   python bin\moral_analyzer input.txt --show-summary
echo.
echo   # Analyze a PDF file:
echo   python bin\moral_analyzer document.pdf --output results.json
echo.
echo   # Run the demonstration:
echo   python demo_moral_analysis.py
echo.
echo Environment '%ENV_NAME%' is now active.
echo To reactivate later, run: conda activate %ENV_NAME%
goto :end

:model_failed
echo.
echo ================================
echo Setup Complete (with warnings)
echo ================================
echo.
echo eMFDscore is installed but spaCy model installation failed.
echo.
echo TROUBLESHOOTING SPACY MODEL ISSUES:
echo.
echo 1. Check your internet connection
echo 2. Try running as administrator
echo 3. Manual installation:
echo    a) Download from: https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
echo    b) Save to your current directory
echo    c) Run: pip install en_core_web_sm-3.8.0-py3-none-any.whl
echo.
echo 4. If wheel is corrupted, try:
echo    - Clear pip cache: pip cache purge
echo    - Use different mirror: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple spacy
echo    - Then try: python -m spacy download en_core_web_sm
echo.
echo 5. Alternative: Install from conda-forge
echo    conda install -c conda-forge spacy-model-en_core_web_sm

:end
echo.
pause