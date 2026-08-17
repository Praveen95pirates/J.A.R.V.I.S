@echo off
setlocal
echo ============================================================
echo J.A.R.V.I.S. - GitHub Push Helper
echo ============================================================
echo.

cd /d "C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S"

echo [Step 1] Initializing Git repository...
git init
echo Done.
echo.

echo [Step 2] Adding all files...
git add .
echo Done.
echo.

echo [Step 3] Creating first commit...
git commit -m "Initial commit: J.A.R.V.I.S. with voice, trading skills, and Android APK support"
echo Done.
echo.

echo [Step 4] Renaming branch to main...
git branch -M main
echo Done.
echo.

echo ============================================================
echo IMPORTANT: Edit the remote URL below with YOUR username!
echo ============================================================
echo.
echo Current command:
echo git remote add origin https://github.com/YOUR_USERNAME/J.A.R.V.I.S.git
echo.
echo Replace YOUR_USERNAME with your actual GitHub username
echo.
pause

echo [Step 5] Adding remote repository...
set /p github_user="Enter your GitHub username: "
git remote add origin https://github.com/%github_user%/J.A.R.V.I.S.git
echo Done.
echo.

echo [Step 6] Pushing to GitHub...
git push -u origin main
echo Done.
echo.

echo ============================================================
echo SUCCESS! Your repository is now on GitHub
echo ============================================================
echo.
echo Next steps:
echo 1. Go to: https://github.com/%github_user%/J.A.R.V.I.S
echo 2. Click "Actions" tab
echo 3. Run "Build J.A.R.V.I.S. Android APK" workflow
echo 4. Download APK from artifacts
echo 5. Install on your phone
echo.
pause
