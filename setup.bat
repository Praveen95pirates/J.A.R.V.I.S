@echo off
setlocal
echo ============================================================
echo J.A.R.V.I.S. Quick Setup
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/4] Creating directories...
if not exist "dist" mkdir dist
if not exist "dist\android" mkdir dist\android
if not exist "data" mkdir data
if not exist "memory" mkdir memory
if not exist "logs" mkdir logs
echo Done.
echo.

echo [2/4] Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Done.
echo.

echo [3/4] Generating Android assets...
python build_apk_assets.py
echo Done.
echo.

echo [4/4] Verifying installation...
python -c "from skills.trading_skills import handle_request; print('Trading backend OK')"
python -c "from skills.skill_manager import get_skill_manager; print('Skill manager OK')"
python -c "from voice.background_voice_assistant import BackgroundVoiceAssistant; print('Voice assistant OK')"
echo Done.
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Test locally: python launcher.py
echo   2. Start web server: python web/web_interface.py
echo   3. Build APK via GitHub Actions (see README.md)
echo.
pause
