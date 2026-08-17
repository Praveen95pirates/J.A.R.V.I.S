#!/usr/bin/env python3
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
