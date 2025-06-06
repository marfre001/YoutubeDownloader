@echo off
setlocal

REM Set the Python "home" to ensure it always finds tkinter and other libraries
set "PYTHONHOME=%~dp0python"
set "PYTHONPATH="

echo Starting the application with the portable Python interpreter...

REM Execute the script using the correct python.exe
"%PYTHONHOME%\python.exe" "%~dp0ytd.py"

echo.
echo The application has been closed. Press any key to exit.
pause
endlocal