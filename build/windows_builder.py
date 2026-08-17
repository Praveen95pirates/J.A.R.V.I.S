#!/usr/bin/env python3
"""
J.A.R.V.I.S Windows Executable Builder
Builds a standalone Windows application with PyInstaller
"""

import os
import sys
import shutil
import subprocess
import platform


class WindowsBuilder:
    """Build J.A.R.V.I.S. as a Windows executable"""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.build_dir = os.path.join(self.project_root, "build", "windows")
        self.dist_dir = os.path.join(self.project_root, "dist", "windows")
    
    def check_requirements(self) -> bool:
        """Check if build requirements are met"""
        if platform.system() != "Windows":
            print("[Builder] ERROR: Windows build must be run on Windows!")
            return False
        
        try:
            import PyInstaller
            print(f"[Builder] PyInstaller {PyInstaller.__version__} found")
            return True
        except ImportError:
            print("[Builder] PyInstaller not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            return True
    
    def create_spec_file(self) -> str:
        """Create PyInstaller spec file"""
        project_root = os.path.abspath(self.project_root).replace("\\", "/")
        main_path = os.path.join(project_root, "main.py").replace("\\", "/")
        config_dir = os.path.join(project_root, "config").replace("\\", "/")
        core_dir = os.path.join(project_root, "core").replace("\\", "/")
        emotions_dir = os.path.join(project_root, "emotions").replace("\\", "/")
        skills_dir = os.path.join(project_root, "skills").replace("\\", "/")
        data_dir = os.path.join(project_root, "data").replace("\\", "/")
        spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{main_path}'],
    pathex=['{project_root}'],
    binaries=[],
    datas=[
        ('{config_dir}', 'config'),
        ('{core_dir}', 'core'),
        ('{emotions_dir}', 'emotions'),
        ('{skills_dir}', 'skills'),
        ('{data_dir}', 'data'),
    ],
    hiddenimports=[
        'pyttsx3',
        'edge_tts',
        'speech_recognition',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'pythoncom',
        'win32api',
        'win32con',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='JARVIS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    runtime_tmpdir=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='JARVIS',
)
"""
        spec_path = os.path.join(self.build_dir, "JARVIS.spec")
        with open(spec_path, "w", encoding="utf-8") as f:
            f.write(spec_content)
        return spec_path
    
    def build(self) -> bool:
        """Build the Windows executable"""
        print("[Builder] Starting Windows build...")
        
        if not self.check_requirements():
            return False
        
        os.makedirs(self.build_dir, exist_ok=True)
        
        # Create spec file
        spec_path = self.create_spec_file()
        print(f"[Builder] Spec file created: {spec_path}")
        
        # Build using PyInstaller with explicit spec path
        print("[Builder] Building executable...")
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--distpath", self.dist_dir, "--workpath", os.path.join(self.build_dir, "work"), spec_path],
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("[Builder] Build successful!")
            print(f"[Builder] Output: {self.dist_dir}")
            
            # Create launcher batch file
            self._create_launcher()
            return True
        else:
            print(f"[Builder] Build failed: {result.stderr}")
            return False
    
    def _create_launcher(self):
        """Create a convenient launcher batch file"""
        launcher_content = """@echo off
title J.A.R.V.I.S. - Just A Rather Very Intelligent System
echo.
echo    J.A.R.V.I.S.
echo    Just A Rather Very Intelligent System
echo.
echo    Initializing systems...
echo.
cd /d "%~dp0"
JARVIS.exe
pause
"""
        launcher_path = os.path.join(self.dist_dir, "Launch JARVIS.bat")
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        print(f"[Builder] Launcher created: {launcher_path}")
    
    def create_installer(self) -> bool:
        """Create an installer using Inno Setup or NSIS"""
        print("[Builder] Creating installer...")
        
        # Create Inno Setup script
        iss_content = f"""; J.A.R.V.I.S. Installer Script
; Generated by JARVIS Builder

[Setup]
AppName=J.A.R.V.I.S.
AppVersion=1.0.0
DefaultDirName={{autopf}}\\J.A.R.V.I.S.
DefaultGroupName=J.A.R.V.I.S.
OutputDir={self.dist_dir}\\installer
OutputBaseFilename=JARVIS-Setup-v1.0.0
Compression=lzma
SolidCompression=yes

[Files]
Source: "{self.dist_dir}\\JARVIS\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{{group}}\\J.A.R.V.I.S."; Filename: "{{app}}\\JARVIS.exe"
Name: "{{commondesktop}}\\J.A.R.V.I.S."; Filename: "{{app}}\\JARVIS.exe"

[Run]
Filename: "{{app}}\\JARVIS.exe"; Description: "Launch J.A.R.V.I.S."; Flags: nowait postinstall skipifsilent
"""
        iss_path = os.path.join(self.build_dir, "installer.iss")
        with open(iss_path, 'w') as f:
            f.write(iss_content)
        
        print(f"[Builder] Installer script created: {iss_path}")
        print("[Builder] To build installer, run: iscc installer.iss")
        return True


def main():
    """Main build entry point"""
    builder = WindowsBuilder()
    
    print("=" * 60)
    print("  J.A.R.V.I.S. Windows Builder")
    print("=" * 60)
    print()
    
    if builder.build():
        print("\n[Builder] Build completed successfully!")
        print(f"[Builder] Executable location: {builder.dist_dir}")
        
        # Try to create installer
        builder.create_installer()
    else:
        print("\n[Builder] Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
