# J.A.R.V.I.S. - GitHub Repository Setup Guide
## Exact Step-by-Step Instructions to Build Your APK

This guide will walk you through setting up a GitHub repository and building the J.A.R.V.I.S. Android APK.

---

## Prerequisites
- GitHub account
- Git installed on your Windows PC
- 30 minutes of time

---

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `J.A.R.V.I.S`
3. Description: `Just A Rather Very Intelligent System - Personal AI Assistant with Voice and Trading Skills`
4. Set to **Public** (required for free GitHub Actions)
5. **DO NOT** check "Add a README file"
6. Click **Create repository**

---

## Step 2: Prepare Your Local Repository

Open **Git Bash** or **Command Prompt** and run:

```bash
# Navigate to your project folder
cd "C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S"

# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: J.A.R.V.I.S. with voice, trading skills, and Android APK support"

# Rename branch to main
git branch -M main

# Add your GitHub repository as remote
# REPLACE YOUR_USERNAME WITH YOUR ACTUAL GITHUB USERNAME
git remote add origin https://github.com/YOUR_USERNAME/J.A.R.V.I.S.git

# Push to GitHub
git push -u origin main
```

**Important:** Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 3: Verify GitHub Actions Workflow

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You should see **"Build J.A.R.V.I.S. Android APK"** workflow
4. Click on it
5. Click **"Run workflow"** button
6. Click **"Run workflow"** again to confirm

---

## Step 4: Monitor the Build

The build will take **15-30 minutes**. You'll see steps like:
- ✓ Checkout code
- ✓ Set up Python 3.11
- ✓ Install system dependencies
- ✓ Install Python dependencies
- ✓ Create app icon and splash
- ✓ Build Debug APK

**Do not close the browser.** You can monitor progress in real-time.

---

## Step 5: Download the APK

Once the build completes:
1. Scroll to the bottom of the workflow run
2. Under **"Artifacts"** section, you'll see **"JARVIS-debug-apk"**
3. Click on it to download
4. Extract the ZIP file
5. You'll get: `JARVIS-debug.apk`

---

## Step 6: Install APK on Your Phone

### On Android:
1. Transfer `JARVIS-debug.apk` to your phone
2. On your phone, go to **Settings > Security**
3. Enable **"Unknown Sources"** or **"Install unknown apps"**
   - If using Chrome: Settings > Apps > Chrome > Install unknown apps > Allow
   - If using Files app: Settings > Apps > Files > Install unknown apps > Allow
4. Open the APK file
5. Click **Install**
6. Wait for installation to complete
7. Click **Open** to launch J.A.R.V.I.S.

---

## Step 7: Configure the App

### Option A: Web Mode (Recommended for Full Features)
1. On your Windows PC, run:
   ```bash
   cd "C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S"
   python web/web_interface.py
   ```

2. The server will start at `http://0.0.0.0:5000`

3. Find your PC's IP address:
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" under your WiFi adapter (e.g., `192.168.1.111`)

4. On Android, open Chrome and go to:
   ```
   http://YOUR_PC_IP:5000
   ```
   Example: `http://192.168.1.111:5000`

### Option B: Standalone App
The APK works in standalone mode with limited features. For full trading features, use web mode.

---

## Troubleshooting

### Build Fails in GitHub Actions
1. Check the **buildozer-logs** artifact for error details
2. Common issues:
   - Missing dependencies: Will be auto-installed
   - Build timeout: Re-run the workflow
   - Icon/splash issues: Run `python build_apk_assets.py` locally and commit

### APK Won't Install
1. Ensure "Unknown Sources" is enabled
2. Check Android version (must be 8.0+)
3. Uninstall old version first if updating
4. Check if APK is corrupted during transfer

### App Won't Start
1. Check internet permissions are granted
2. For web mode, ensure PC and phone are on same WiFi
3. Check firewall allows port 5000

### Voice Not Working
1. Grant microphone permission to the app
2. For web mode, use Chrome browser
3. Ensure internet connection for speech recognition

---

## Updating Skills Automatically

### Method 1: Add Skills to Repository
1. Create a new file in `skills/` directory (e.g., `my_skill.py`)
2. Commit and push to GitHub
3. Re-run GitHub Actions workflow
4. New skill will be auto-discovered

### Method 2: Remote Update via API
Send a POST request to `/api/skill-manager/update`:
```json
{
  "add": [
    {
      "name": "bitcoin_price",
      "category": "TRADING",
      "description": "Get Bitcoin price",
      "code": "def run(): return {'btc': 50000}",
      "enabled": true
    }
  ]
}
```

### Method 3: Enable/Disable Skills
```bash
# Enable a skill
curl -X POST http://YOUR_PC_IP:5000/api/skill-manager/enable \
  -H "Content-Type: application/json" \
  -d '{"name": "crypto_trading"}'

# Disable a skill
curl -X POST http://YOUR_PC_IP:5000/api/skill-manager/disable \
  -H "Content-Type: application/json" \
  -d '{"name": "crypto_trading"}'
```

---

## Future Updates

### Adding New Skills
1. Create skill file in `skills/` directory
2. Follow this template:
   ```python
   from skills.skills_registry import Skill, SkillCategory
   
   def register_skills(registry):
       registry.register(Skill(
           name="my_new_skill",
           category=SkillCategory.SYSTEM,
           description="What this skill does",
           enabled=True
       ))
   ```

3. Commit and push
4. GitHub Actions will rebuild APK automatically

### Updating Trading Skills
Edit `skills/trading_skills.py` to add:
- New broker integrations
- Additional technical indicators
- Enhanced risk management
- Real API connections

### Adding Real Broker APIs
In `skills/trading_skills.py`, replace simulated functions with real API calls:

```python
# Example: Zerodha integration
import kiteconnect

def connect_zerodha(api_key, api_secret):
    kite = kiteconnect.KiteConnect(api_key=api_key)
    # Get request token from user
    # Generate access token
    return kite

def get_zerodha_portfolio(kite):
    return kite.holdings()
```

---

## Maintenance

### Regular Updates
- Push code changes to GitHub
- Re-run GitHub Actions to rebuild APK
- Download and install new APK

### Monitoring
- Check GitHub Actions logs for build errors
- Monitor app performance on device
- Review trading skill accuracy

### Backup
- Your repository on GitHub is your backup
- All skills are in the `skills/` directory
- Configuration in `config/project.yaml`

---

## Support

If you encounter issues:
1. Check the **buildozer-logs** artifact in GitHub Actions
2. Review this guide's troubleshooting section
3. Ensure all prerequisites are met
4. Re-run the workflow after fixing issues

---

## Next Steps After Installation

1. **Configure server URL** in `android/main.py`:
   ```python
   SERVER_URL = "http://YOUR_PC_IP:5000"
   ```

2. **Start the web server** on your PC:
   ```bash
   python web/web_interface.py
   ```

3. **Connect Android app** to server:
   - Open app on phone
   - Ensure same WiFi network
   - App will auto-connect to server

4. **Test voice commands**:
   - Tap microphone button
   - Say "JARVIS, what's the price of Reliance?"
   - Or type in chat

5. **Explore trading features**:
   - Go to Trading tab
   - Try Quotes, Technical Analysis, Portfolio
   - Test paper trading

---

## Congratulations!

You now have:
- ✓ J.A.R.V.I.S. Android app installed
- ✓ Voice recognition with wake word
- ✓ 91 skills including trading/broker capabilities
- ✓ Automatic skill update system
- ✓ GitHub repository for future updates

**Your J.A.R.V.I.S. is ready to use!**

---

*Generated on: August 17, 2026*
*Version: 1.0.0*
