#!/usr/bin/env python3
"""
Generate Android APK assets and packaging scripts
"""

import os
import sys
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
ANDROID_DIR = PROJECT_ROOT / "android"


def create_splash_image():
    """Create a simple splash screen placeholder"""
    print("[APK] Creating splash screen...")
    
    # Create a simple 1x1 transparent PNG as placeholder
    # In a real project, you would replace this with a proper splash image
    splash_path = ANDROID_DIR / "app" / "src" / "main" / "res" / "drawable" / "splash.png"
    
    # Minimal valid PNG file (1x1 transparent pixel)
    png_data = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
        b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    
    with open(splash_path, 'wb') as f:
        f.write(png_data)
    
    print(f"[APK] Splash created: {splash_path}")


def create_icon_image():
    """Create a simple icon placeholder"""
    print("[APK] Creating icon placeholder...")
    
    icon_path = ANDROID_DIR / "app" / "src" / "main" / "res" / "drawable" / "icon.png"
    
    # Minimal valid PNG file (1x1 transparent pixel)
    png_data = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
        b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    
    with open(icon_path, 'wb') as f:
        f.write(png_data)
    
    print(f"[APK] Icon created: {icon_path}")


def create_apk_build_script():
    """Create a script to build the APK"""
    print("[APK] Creating build script...")
    
    script_path = PROJECT_ROOT / "build_apk.py"
    
    script = '''#!/usr/bin/env python3
"""
J.A.R.V.I.S. APK Builder
Builds the Android application package
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
ANDROID_DIR = PROJECT_ROOT / "android"
BUILD_DIR = PROJECT_ROOT / "dist" / "android"


def check_buildozer():
    """Check if buildozer is installed"""
    try:
        subprocess.run(['buildozer', '--version'], capture_output=True, check=True)
        print("[Build] Buildozer is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[Build] Buildozer not found. Install with: pip install buildozer")
        return False


def check_adb():
    """Check if ADB is available"""
    try:
        subprocess.run(['adb', 'version'], capture_output=True, check=True)
        print("[Build] ADB is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[Build] ADB not found. Install Android SDK platform tools.")
        return False


def build_apk():
    """Build the APK using buildozer"""
    print("[Build] Starting APK build...")
    
    os.chdir(ANDROID_DIR)
    
    # Initialize buildozer if needed
    buildozer_spec = ANDROID_DIR / "buildozer.spec"
    if not buildozer_spec.exists():
        print("[Build] Initializing buildozer...")
        subprocess.run(['buildozer', 'init'], check=True)
    
    # Build debug APK
    print("[Build] Building debug APK...")
    subprocess.run([
        'buildozer',
        'android', 'debug',
        '--profile', 'default'
    ], check=True)
    
    # Copy APK to dist
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    
    bin_dir = ANDROID_DIR / "bin"
    if bin_dir.exists():
        for apk in bin_dir.glob("*.apk"):
            dest = BUILD_DIR / apk.name
            shutil.copy(apk, dest)
            print(f"[Build] APK copied to: {dest}")
            return dest
    
    print("[Build] APK build completed")
    return None


def build_with_gradle():
    """Alternative build using Gradle directly"""
    print("[Build] Starting Gradle build...")
    
    os.chdir(ANDROID_DIR)
    
    # Check for Gradle wrapper
    if not (ANDROID_DIR / "gradlew").exists():
        print("[Build] Gradle wrapper not found")
        return None
    
    # Build debug APK
    print("[Build] Building debug APK with Gradle...")
    subprocess.run([
        './gradlew',
        'assembleDebug'
    ], check=True)
    
    # Copy APK to dist
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    
    apk_path = ANDROID_DIR / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
    if apk_path.exists():
        dest = BUILD_DIR / "JARVIS-debug.apk"
        shutil.copy(apk_path, dest)
        print(f"[Build] APK copied to: {dest}")
        return dest
    
    return None


def main():
    """Main build function"""
    print("=" * 60)
    print("J.A.R.V.I.S. APK Builder")
    print("=" * 60)
    print()
    
    print("[Build] Prerequisites:")
    print("  - Python 3.8+")
    print("  - Buildozer: pip install buildozer")
    print("  - Android SDK: https://developer.android.com/studio")
    print("  - ADB: part of Android SDK platform-tools")
    print()
    
    # Check prerequisites
    buildozer_available = check_buildozer()
    adb_available = check_adb()
    
    if not buildozer_available:
        print("[Build] Buildozer is required for APK building")
        print("[Build] Install with: pip install buildozer")
        sys.exit(1)
    
    # Build APK
    try:
        apk_path = build_apk()
        if apk_path:
            print()
            print("=" * 60)
            print(f"SUCCESS! APK ready: {apk_path}")
            print("=" * 60)
            print()
            print("To install on your phone:")
            print(f"  adb install {apk_path}")
            print()
            print("Or transfer the APK to your phone and install manually")
        else:
            print("[Build] Build completed but APK location unknown")
    except Exception as e:
        print(f"[Build] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
'''
    
    with open(script_path, 'w') as f:
        f.write(script)
    
    script_path.chmod(0o755)
    print(f"[APK] Build script created: {script_path}")


def create_github_actions():
    """Create GitHub Actions workflow for APK building"""
    print("[APK] Creating GitHub Actions workflow...")
    
    workflow_dir = PROJECT_ROOT / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_path = workflow_dir / "build-apk.yml"
    
    workflow = '''name: Build J.A.R.V.I.S. Android APK

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Buildozer
        run: |
          sudo apt-get update
          sudo apt-get install -y python3-pip autoconf automake libtool pkg-config
          pip3 install --upgrade pip
          pip3 install buildozer cython==0.29.33

      - name: Initialize Buildozer
        working-directory: ./android
        run: |
          cp buildozer.spec buildozer.spec.bak || true
          if [ ! -f buildozer.spec ]; then
            buildozer init
            cp buildozer.spec.bak buildozer.spec 2>/dev/null || true
          fi

      - name: Build Debug APK
        working-directory: ./android
        run: |
          buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: JARVIS-debug-apk
          path: android/bin/*.apk
          retention-days: 30

      - name: Upload Logs
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: buildozer-logs
          path: android/.buildozer/logs/
          retention-days: 7
'''
    
    with open(workflow_path, 'w') as f:
        f.write(workflow)
    
    print(f"[APK] GitHub Actions workflow created: {workflow_path}")


def create_pwa_interface():
    """Create a PWA-style web interface that can be installed"""
    print("[APK] Creating PWA installer interface...")
    
    pwa_dir = PROJECT_ROOT / "web" / "pwa"
    pwa_dir.mkdir(parents=True, exist_ok=True)
    
    # Service Worker
    sw = pwa_dir / "service-worker.js"
    sw.write_text('''self.addEventListener('install', (e) => {
  console.log('[SW] Install');
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  console.log('[SW] Activate');
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
''')
    
    print(f"[PWA] Service worker created: {sw}")


def update_main_with_wake_word():
    """Update main.py to include wake word detection"""
    print("[Voice] Updating main.py with wake word detection...")
    
    main_path = PROJECT_ROOT / "main.py"
    content = main_path.read_text()
    
    # Add wake word detection imports and setup
    if "wake_word" not in content:
        # Add after the imports
        lines = content.split('\n')
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.startswith('from voice.voice_engine import JARVISVoiceAssistant'):
                new_lines.append('')
                new_lines.append('# Wake word configuration')
                new_lines.append('WAKE_WORD = "jarvis"')
                new_lines.append('WAKE_WORD_VARIANTS = ["jarvis", "hey jarvis", "ok jarvis", "jarvis please"]')
        
        main_path.write_text('\n'.join(new_lines))
        print("[Voice] Wake word configuration added")


def main():
    """Main asset generation"""
    print("=" * 60)
    print("J.A.R.V.I.S. APK Asset Generator")
    print("=" * 60)
    print()
    
    create_splash_image()
    create_icon_image()
    create_apk_build_script()
    create_github_actions()
    create_pwa_interface()
    update_main_with_wake_word()
    
    print()
    print("=" * 60)
    print("Asset generation complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review android/buildozer.spec")
    print("2. Install buildozer: pip install buildozer")
    print("3. Build APK: cd android && buildozer android debug")
    print("4. Or use GitHub Actions workflow")
    print()


if __name__ == '__main__':
    main()
