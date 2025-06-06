@echo off
setlocal
title FFmpeg Guided Installation

REM --- CONFIGURATION ---
REM Official URL for FFmpeg download (Windows 64-bit "essentials" build)
set "FFMPEG_URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
REM Name of the zip file that will be downloaded
set "ZIP_NAME=ffmpeg.zip"
REM Installation folder (inside AppData\Local, does not require admin rights)
set "INSTALL_DIR=%LOCALAPPDATA%\FFmpeg"
REM --------------------

cls
echo =================================================================
echo  Automatic FFmpeg Installation for the Application
echo =================================================================
echo.
echo This script will download and install FFmpeg, a component
echo required for the app to function correctly.
echo.
echo The installation will take place in: %INSTALL_DIR%
echo.
echo It will also modify your user's 'PATH' environment variable
echo to make FFmpeg always available.
echo.
echo An internet connection is required.
echo.

:CONFIRM
choice /C YN /M "Do you want to proceed with the installation?"
if errorlevel 2 (
    echo.
    echo Installation canceled by the user.
    goto :EOF
)

cls
echo Starting procedure...

REM --- 1. CHECK IF FFMPEG IS ALREADY INSTALLED ---
echo.
echo [1/5] Checking if FFmpeg is already in the PATH...
echo %PATH% | find /I "ffmpeg" >nul
if %errorlevel% == 0 (
    echo      -> Found! FFmpeg appears to be already configured.
    echo      -> No action needed.
    goto :SUCCESS
) else (
    echo      -> Not found. Proceeding with installation.
)

REM --- 2. DOWNLOAD FFMPEG ---
echo.
echo [2/5] Downloading FFmpeg...
echo      (This may take a moment)
powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri '%FFMPEG_URL%' -OutFile '%ZIP_NAME%'"
if not exist "%ZIP_NAME%" (
    echo      -> ERROR: FFmpeg download failed. Check your connection.
    goto :FAIL
)
echo      -> Download complete.

REM --- 3. CREATE FOLDER AND UNZIP ---
echo.
echo [3/5] Unzipping files to %INSTALL_DIR%...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Path '%ZIP_NAME%' -DestinationPath '%INSTALL_DIR%' -Force"
if errorlevel 1 (
    echo      -> ERROR: Unzipping failed.
    goto :FAIL
)

REM --- 4. FIND THE 'BIN' FOLDER AND ADD TO PATH ---
echo.
echo [4/5] Configuring the path (PATH)...

REM The zip file creates a subfolder with a variable name (e.g., ffmpeg-6.0-essentials_build)
REM This for loop finds the name of that folder.
set "FFMPEG_EXTRACTED_DIR="
for /d %%i in ("%INSTALL_DIR%\ffmpeg-*") do set "FFMPEG_EXTRACTED_DIR=%%i"

if not defined FFMPEG_EXTRACTED_DIR (
    echo      -> ERROR: Could not find the unzipped FFmpeg folder.
    goto :FAIL
)

set "FFMPEG_BIN_PATH=%FFMPEG_EXTRACTED_DIR%\bin"

REM Permanently adds the path to the USER's PATH.
setx PATH "%FFMPEG_BIN_PATH%;%PATH%"
echo      -> Path %FFMPEG_BIN_PATH% added successfully.

REM --- 5. CLEANUP ---
echo.
echo [5/5] Cleaning up temporary files...
if exist "%ZIP_NAME%" del "%ZIP_NAME%"
echo      -> Cleanup complete.

goto :SUCCESS

:SUCCESS
echo.
echo =================================================================
echo  OPERATION COMPLETED SUCCESSFULLY!
echo =================================================================
echo.
echo FFmpeg has been installed and configured.
echo.
echo IMPORTANT: To apply the changes, you may need to
echo RESTART this terminal window or, in some cases,
echo restart your computer.
echo.
goto :END

:FAIL
echo.
echo =================================================================
echo  ERROR DURING INSTALLATION
echo =================================================================
echo.
echo Something went wrong. Please try running the script again.
echo If the error persists, contact support.
echo.
goto :END

:END
pause