@echo off
title J.A.R.V.I.S. Setup
echo.
echo    J.A.R.V.I.S. Setup
echo    Just A Rather Very Intelligent System
echo.
echo    This will create a portable JARVIS package.
echo.
pause

echo.
echo [1/3] Creating portable package...
if not exist "JARVIS_Portable" mkdir "JARVIS_Portable"
if not exist "JARVIS_Portable\config" mkdir "JARVIS_Portable\config"
if not exist "JARVIS_Portable\core" mkdir "JARVIS_Portable\core"
if not exist "JARVIS_Portable\emotions" mkdir "JARVIS_Portable\emotions"
if not exist "JARVIS_Portable\skills" mkdir "JARVIS_Portable\skills"
if not exist "JARVIS_Portable\data" mkdir "JARVIS_Portable\data"
if not exist "JARVIS_Portable\voice" mkdir "JARVIS_Portable\voice"
if not exist "JARVIS_Portable\web" mkdir "JARVIS_Portable\web"
if not exist "JARVIS_Portable\build" mkdir "JARVIS_Portable\build"

echo [2/3] Copying files...
xcopy /E /I /Y "config\*.*" "JARVIS_Portable\config\"
xcopy /E /I /Y "core\*.*" "JARVIS_Portable\core\"
xcopy /E /I /Y "emotions\*.*" "JARVIS_Portable\emotions\"
xcopy /E /I /Y "skills\*.*" "JARVIS_Portable\skills\"
xcopy /E /I /Y "data\*.*" "JARVIS_Portable\data\"
xcopy /E /I /Y "voice\*.*" "JARVIS_Portable\voice\"
xcopy /E /I /Y "web\*.*" "JARVIS_Portable\web\"
xcopy /E /I /Y "build\*.*" "JARVIS_Portable\build\"
copy /Y "main.py" "JARVIS_Portable\"
copy /Y "launcher.py" "JARVIS_Portable\"
copy /Y "requirements.txt" "JARVIS_Portable\"
copy /Y "README.md" "JARVIS_Portable\"

echo [3/3] Creating launchers...
echo @echo off > "JARVIS_Portable\Start JARVIS.bat"
echo cd /d "%%~dp0" >> "JARVIS_Portable\Start JARVIS.bat"
echo python main.py >> "JARVIS_Portable\Start JARVIS.bat"
echo pause >> "JARVIS_Portable\Start JARVIS.bat"

echo @echo off > "JARVIS_Portable\Start JARVIS Web.bat"
echo cd /d "%%~dp0" >> "JARVIS_Portable\Start JARVIS Web.bat"
echo python web\web_interface.py >> "JARVIS_Portable\Start JARVIS Web.bat"
echo pause >> "JARVIS_Portable\Start JARVIS Web.bat"

echo @echo off > "JARVIS_Portable\Install Dependencies.bat"
echo echo Installing dependencies... >> "JARVIS_Portable\Install Dependencies.bat"
echo pip install -r requirements.txt >> "JARVIS_Portable\Install Dependencies.bat"
echo pause >> "JARVIS_Portable\Install Dependencies.bat"

echo.
echo ========================================================
echo    Setup Complete!
echo ========================================================
echo.
echo    Portable package created: JARVIS_Portable\
echo.
echo    To use:
echo    1. Copy the JARVIS_Portable folder anywhere
echo    2. Run "Install Dependencies.bat" once
echo    3. Run "Start JARVIS.bat" for CLI mode
echo    4. Run "Start JARVIS Web.bat" for Android/browser mode
echo.
echo    Android URL: http://YOUR_PC_IP:5000
echo.
pause
