# J.A.R.V.I.S. - Public Repository Checklist
## Minimal Steps to Ensure GitHub Actions Builds Without Issues

Use this checklist before making your repo public and triggering the APK build.

---

## Pre-Flight Check (Do These First)

### 1. Repository Settings
- [ ] Repository name is exactly: `J.A.R.V.I.S`
- [ ] Repository is **Public** (GitHub Actions free tier requires public repos)
- [ ] **DO NOT** initialize with README, .gitignore, or license
- [ ] Repository is empty before first push

### 2. Required Files Check
Verify these files exist in your project:
```bash
cd "C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S"
dir .github\workflows\build-apk.yml
dir android\buildozer.spec
dir android\main.py
dir requirements.txt
dir setup.bat
dir push_to_github.bat
```

All must exist before pushing.

### 3. Git Configuration
```bash
cd "C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S"

# Check git is installed
git --version

# Initialize if not already done
git init

# Configure git (replace with your info)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 4. Verify No Large Files
```bash
# Check for files larger than 100MB (GitHub limit is 100MB)
git ls-files | xargs ls -lS | awk '$5 > 100000000'
```

If any files are too large, add them to `.gitignore`:
```bash
echo "*.mp3" >> .gitignore
echo "*.wav" >> .gitignore
echo "*.apk" >> .gitignore
echo "build/" >> .gitignore
echo "dist/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

---

## Push to GitHub (Exact Commands)

```bash
cd "C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S"

# Stage all files
git add .

# Commit
git commit -m "Initial commit: J.A.R.V.I.S. with voice, trading skills, and Android APK support"

# Set branch name
git branch -M main

# Add remote (REPLACE YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/J.A.R.V.I.S.git

# Push
git push -u origin main
```

---

## Post-Push Verification

### 5. Verify Repository on GitHub
1. Go to `https://github.com/YOUR_USERNAME/J.A.R.V.I.S`
2. Confirm these files are visible:
   - [ ] `.github/workflows/build-apk.yml`
   - [ ] `android/buildozer.spec`
   - [ ] `android/main.py`
   - [ ] `requirements.txt`
   - [ ] `README.md`

### 6. Verify GitHub Actions Workflow
1. Click **Actions** tab
2. You should see **"Build J.A.R.V.I.S. Android APK"** in the left sidebar
3. If not visible:
   - Go to **Settings** > **Actions** > **General**
   - Ensure "Allow all actions and reusable workflows" is selected
   - Wait 1-2 minutes for workflow to appear

---

## Trigger the Build

### 7. First Build
1. Go to **Actions** tab
2. Click **"Build J.A.R.V.I.S. Android APK"**
3. Click **"Run workflow"** button
4. Select branch: **main**
5. Click **"Run workflow"** again

### 8. Monitor Build Progress
Watch these steps complete:
- [ ] **Checkout code** (1 min)
- [ ] **Set up Python 3.11** (1 min)
- [ ] **Install system dependencies** (3-5 mins)
- [ ] **Install Python dependencies** (2-3 mins)
- [ ] **Create app icon and splash** (30 sec)
- [ ] **Initialize Buildozer** (1 min)
- [ ] **Build Debug APK** (10-20 mins) ⚠️ Longest step
- [ ] **Upload Debug APK** (1 min)

**Total time: 20-30 minutes**

---

## Common Build Issues & Fixes

### Issue: Workflow doesn't appear
**Fix:**
1. Check repository is **Public**
2. Wait 2-3 minutes after push
3. Refresh browser
4. Check Settings > Actions > General

### Issue: Build fails at "Install system dependencies"
**Fix:**
- This is usually a transient network issue
- Re-run the workflow
- Check GitHub status page

### Issue: Build fails at "Build Debug APK"
**Fix:**
1. Download **buildozer-logs** artifact
2. Look for error messages
3. Common fixes:
   - Missing icon: Run `python build_apk_assets.py` locally and commit
   - Permission errors: Check `android/buildozer.spec` has correct permissions
   - Timeout: Re-run workflow

### Issue: APK artifact not found
**Fix:**
- Ensure build reached "Upload Debug APK" step
- Check artifact name is `JARVIS-debug-apk`
- Re-run workflow if artifact upload failed

---

## Download & Install APK

### 9. Download APK
1. Once build completes, scroll to **Artifacts** section
2. Click **JARVIS-debug-apk**
3. Download ZIP file
4. Extract to get `JARVIS-debug.apk`

### 10. Transfer to Phone
**Method A: Direct Download**
1. On phone, open browser
2. Go to your GitHub repo
3. Download artifact directly

**Method B: USB Transfer**
1. Connect phone to PC via USB
2. Copy `JARVIS-debug.apk` to phone storage
3. Disconnect USB

### 11. Install APK
1. On phone, open file manager
2. Navigate to downloaded APK
3. Tap to install
4. If prompted, enable "Install unknown sources"
5. Tap "Install"
6. Wait for installation
7. Tap "Open"

---

## Post-Installation Setup

### 12. Configure Server Connection
1. On Windows PC, start web server:
   ```bash
   cd "C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S"
   python web/web_interface.py
   ```

2. Find your PC's IP address:
   ```bash
   ipconfig
   ```
   Look for IPv4 under WiFi adapter (e.g., `192.168.1.111`)

3. On Android app:
   - The app connects to `http://192.168.1.111:5000` by default
   - If your IP is different, edit `android/main.py` line with `SERVER_URL`
   - Rebuild APK if IP changed

### 13. Test Features
- [ ] Open app
- [ ] Navigate between Chat, Trading, Skills tabs
- [ ] Send a test message
- [ ] Test voice button (requires microphone permission)
- [ ] Test trading features (requires server connection)
- [ ] Test skills listing

---

## Future Updates

### Adding New Skills
1. Create new file in `skills/` directory
2. Commit and push to GitHub
3. Re-run GitHub Actions workflow
4. Download and install new APK

### Updating Code
1. Make changes locally
2. Commit and push:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
3. Re-run GitHub Actions workflow
4. Download and install new APK

### Automatic Rebuilds (Optional)
Set up GitHub Actions to auto-build on push:
```bash
# This is already configured in build-apk.yml
# Every push to main/master will trigger a build
```

---

## Quick Reference

### Important URLs
- **Your repo:** `https://github.com/YOUR_USERNAME/J.A.R.V.I.S`
- **Actions tab:** `https://github.com/YOUR_USERNAME/J.A.R.V.I.S/actions`
- **Web interface:** `http://YOUR_PC_IP:5000`

### Important Paths
- **Project folder:** `C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S`
- **APK output:** `C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S\dist\android\` (after local build)
- **GitHub artifacts:** Download from Actions tab

### Key Commands
```bash
# Start web server
python web/web_interface.py

# Test locally
python launcher.py

# Generate assets
python build_apk_assets.py

# Run setup
setup.bat

# Push to GitHub
push_to_github.bat
```

---

## Emergency Fixes

### If Everything Breaks
1. **Keep local copy safe:** Your `C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S` folder is your master copy
2. **GitHub is backup:** Your repo on GitHub is your remote backup
3. **Restore from GitHub:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/J.A.R.V.I.S.git
   ```

### If APK Won't Install
1. Uninstall old version first
2. Clear Play Protect data
3. Reboot phone
4. Try installing again

### If Voice Doesn't Work
1. Check microphone permissions
2. Use Chrome browser for web mode
3. Ensure internet connection for speech recognition

---

## Success Criteria

You're done when:
- [ ] GitHub repository is public and accessible
- [ ] GitHub Actions workflow appears and runs successfully
- [ ] APK artifact downloads without errors
- [ ] APK installs on Android phone
- [ ] App opens and shows Chat/Trading/Skills tabs
- [ ] Web server connects from phone
- [ ] Voice commands work (with wake word "JARVIS")
- [ ] Trading features display data

---

## Support Checklist

If you need help:
1. [ ] Check this guide's troubleshooting section
2. [ ] Review GitHub Actions logs
3. [ ] Check buildozer-logs artifact
4. [ ] Verify all prerequisites are met
5. [ ] Re-run workflow after fixes
6. [ ] Ensure repository is public
7. [ ] Check GitHub Actions quota hasn't been exceeded

---

## Notes
- GitHub Actions free tier: 500 minutes/month for public repos
- Each APK build takes ~20-30 minutes
- You can build ~15-20 APKs per month on free tier
- For unlimited builds, consider GitHub Pro or self-hosted runner

---

**Last Updated:** August 17, 2026  
**Version:** 1.0.0  
**Compatible with:** J.A.R.V.I.S. v1.0.0+
