#!/usr/bin/env python3
"""
J.A.R.V.I.S. Unified Launcher
Launch CLI, Web Server, or Windows Builder
"""

import os
import sys
import subprocess
import platform

def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║  J.A.R.V.I.S. Launcher - v1.0.0                          ║
    ║  Choose a mode to launch                                 ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_cli():
    """Run CLI mode"""
    print("Starting J.A.R.V.I.S. CLI mode...")
    from main import main
    main()

def run_web():
    """Run web interface"""
    print("Starting J.A.R.V.I.S. web server...")
    from web.web_interface import main as web_main
    web_main()

def run_windows_build():
    """Build Windows executable"""
    print("Building Windows executable...")
    from build.windows_builder import main as build_main
    build_main()

def show_platform_info():
    """Show platform information"""
    print(f"\nPlatform: {platform.system()}")
    print(f"Python: {sys.version}")
    
    # Check dependencies
    deps = {
        'pyttsx3': 'Voice synthesis',
        'edge_tts': 'High-quality voice',
        'SpeechRecognition': 'Voice input',
        'flask': 'Web interface',
        'PyInstaller': 'Windows build'
    }
    
    print("\nDependencies:")
    for mod, desc in deps.items():
        try:
            __import__(mod)
            print(f"  [OK] {mod}: {desc}")
        except ImportError:
            print(f"  [--] {mod}: {desc} (not installed)")

def main():
    print_banner()
    show_platform_info()
    
    print("\n" + "="*60)
    print("  Select Mode:")
    print("="*60)
    print("  1. CLI Mode (Terminal chat with voice)")
    print("  2. Web Server (Browser/Android interface)")
    print("  3. Windows Build (Create .exe)")
    print("  4. Exit")
    print("="*60)
    
    while True:
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == '1':
                run_cli()
                break
            elif choice == '2':
                run_web()
                break
            elif choice == '3':
                run_windows_build()
                break
            elif choice == '4':
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter 1-4.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
