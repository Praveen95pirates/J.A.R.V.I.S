# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S\main.py'],
    pathex=['C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S'],
    binaries=[],
    datas=[
        ('C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S\config', 'config'),
        ('C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S\core', 'core'),
        ('C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S\emotions', 'emotions'),
        ('C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S\skills', 'skills'),
        ('C:\Users\PRAVEENKUMAR V\J.A.R.V.I.S\data', 'data'),
    ],
    hiddenimports=[
        'pyttsx3',
        'edge_tts',
        'speech_recognition',
    ],
    hookspath=[],
    hooksconfig={},
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
