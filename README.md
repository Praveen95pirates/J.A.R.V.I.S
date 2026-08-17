# J.A.R.V.I.S. - Just A Rather Very Intelligent System

> Personal AI assistant with JARVIS-style voice, emotions, 80+ skills, trading/broker capabilities, Android APK support, and automatic skill updates.

## 🚀 Quick Setup (Windows)

Run the setup script:
```bash
setup.bat
```

Or manually:
```bash
pip install -r requirements.txt
python build_apk_assets.py
python launcher.py
```

## 📱 Android APK (Android 10+)

### Option 1: GitHub Actions (Recommended - Works on Windows)
1. Push this repo to GitHub
2. Go to **Actions** tab
3. Run **"Build J.A.R.V.I.S. Android APK"** workflow
4. Download `.apk` from workflow artifacts
5. Install on phone (enable "Install unknown sources")

### Option 2: Local Build (Linux/WSL only)
```bash
cd android
buildozer android debug
```

**APK Details:**
- Min SDK: 21 (Android 5.0)
- Target SDK: 34 (Android 14)
- Compatible with Android 10+
- Includes voice, chat, trading, skills tabs

## 🧠 All Skills (80+)

### Core & Intelligence
- conversation, reasoning, learning, memory_management, context_awareness

### Productivity
- task_management, note_taking, reminder_setting, calendar_management
- time_tracking, goal_setting, project_management

### Creativity
- writing, code_generation, brainstorming, storytelling, poetry
- music_generation, design_thinking

### Analysis
- research, data_analysis, summarization, trend_analysis
- comparison, risk_assessment, weather, news, calculation

### Communication
- email_management, messaging, phone_calls, meeting_scheduling
- translation, presentation_creation

### System Control
- file_management, computer_control, web_browsing, system_automation
- app_control, media_control, screenshot, system_monitoring

### Emotional Support
- emotional_support, mood_tracking, motivation, stress_management
- mindfulness, relationship_advice, crisis_support

### Automation
- workflow_automation, scheduled_tasks, email_automation
- backup_automation, report_generation

### Learning
- skill_acquisition, knowledge_building, tutoring
- language_learning, reading_comprehension

### Security & Privacy
- password_generation, security_advice, privacy_protection

### Finance & Trading (NEW)
- market_data, stock_quotes, crypto_trading, forex_trading
- technical_analysis, portfolio_tracking, risk_management
- trade_execution, broker_integration, options_analytics
- futures_analytics, backtesting, paper_trading
- alert_management, economic_calendar, news_sentiment
- mutual_funds, bond_analytics, tax_reporting
- commodities_trading, trading_journal, algo_trading

## 🎤 Voice Features

- **Wake Word:** Say "JARVIS" to activate
- **Voice Mode:** Continuous listening with wake word detection
- **JARVIS Voice:** British male voice via Edge TTS
- **Offline Fallback:** pyttsx3 for offline TTS
- **Speech Recognition:** Google Speech API + Vosk offline support

## 🔄 Automatic Skill Updates

J.A.R.V.I.S. supports automatic skill discovery and remote updates:

### Auto-Discovery
- New skills placed in `skills/` directory are auto-loaded
- No manual registration needed for new skill files

### Remote Updates
Send a POST request to `/api/skill-manager/update`:
```json
{
  "add": [
    {
      "name": "new_skill",
      "category": "SYSTEM",
      "description": "New capability",
      "code": "def run(): return 'done'",
      "enabled": true
    }
  ],
  "update": [...],
  "remove": [...]
}
```

### Skill Management API
- `GET /api/skill-manager/skills` - List all skills
- `POST /api/skill-manager/enable` - Enable skill
- `POST /api/skill-manager/disable` - Disable skill
- `POST /api/skill-manager/update` - Remote skill update

## 🛠️ Project Structure

```
J.A.R.V.I.S/
├── launcher.py                  # Unified launcher
├── main.py                      # CLI mode
├── requirements.txt             # Dependencies
├── setup.bat                    # Windows setup script
├── config/
│   └── project.yaml             # Configuration
├── core/
│   ├── jarvis_core.py           # Core system
│   └── personality.py           # Personality engine
├── emotions/
│   └── emotional_intelligence.py # Emotional AI
├── skills/
│   ├── skills_registry.py       # Skill definitions
│   ├── complete_skills_library.py # All 80+ skills
│   ├── trading_skills.py        # Trading/broker backend
│   ├── skill_manager.py         # Auto-discovery & updates
│   └── [other skills].py        # Individual skill modules
├── voice/
│   ├── voice_engine.py          # TTS + recognition
│   ├── background_voice_assistant.py # Wake-word voice
│   └── jarvis_voice_profile.py  # Voice config
├── web/
│   ├── web_interface.py         # Flask server
│   └── templates/
│       ├── index.html           # Chat UI
│       └── install.html         # PWA installer
├── android/
│   ├── main.py                  # Kivy Android app
│   ├── buildozer.spec           # Build config
│   └── app/src/main/
│       └── AndroidManifest.xml  # Android manifest
├── build/
│   └── windows_builder.py       # Windows builder
├── .github/
│   └── workflows/
│       └── build-apk.yml        # GitHub Actions APK build
└── dist/
    └── android/                 # APK output
```

## 📊 System Requirements

### Windows
- Windows 10/11
- Python 3.8+
- 4GB RAM
- Microphone (for voice)

### Android
- Android 8.0+ (Oreo)
- Chrome browser or J.A.R.V.I.S. app
- Microphone (for voice)
- Same WiFi as PC for web mode

## 🎯 Usage Examples

### CLI Mode
```bash
python launcher.py
# Select option 1
> help
> status
> skills
> voice on
```

### Web Mode (Android Browser)
```bash
python launcher.py
# Select option 2
# Open http://YOUR_PC_IP:5000 on Android
```

### Android App
```bash
# Install APK from GitHub Actions
# Open J.A.R.V.I.S. app
# Select Chat, Trading, or Skills tab
# Tap microphone for voice input
```

### Voice Commands
```
You: JARVIS, what's the price of Reliance?
J.A.R.V.I.S.: Reliance is currently trading at 2,515 rupees, up 0.5 percent.

You: JARVIS, show me technical analysis for TCS
J.A.R.V.I.S.: TCS shows RSI at 62, MACD bullish cross. Trend: bullish.

You: JARVIS, what's my portfolio value?
J.A.R.V.I.S.: Your portfolio value is 5 lakh rupees with zero unrealized P&L.
```

## 🔧 Configuration

Edit `config/project.yaml`:
```yaml
jarvis:
  personality:
    helpfulness: 1.0
    empathy: 0.9
    humor: 0.6

server:
  host: 0.0.0.0
  port: 5000

trading:
  paper_balance: 500000
  default_broker: zerodha
```

## 🤝 Support

For issues:
1. Check logs in `logs/` directory
2. Run `setup.bat` to verify installation
3. Check GitHub Actions logs for APK build issues
4. Ensure same WiFi network for Android web mode

## 📝 License

Part of J.A.R.V.I.S. Personal Assistant System

---

**J.A.R.V.I.S. - Just A Rather Very Intelligent System**
*Your emotionally intelligent AI companion with voice and trading skills*
