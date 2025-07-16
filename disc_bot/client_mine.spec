# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['client_mine.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\minescore_project\\disc_bot\\minefiles\\server.jar', '.'), ('C:\\minescore_project\\disc_bot\\minefiles\\TLauncher-Installer-1.8.5.exe', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='client_mine',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='client_mine',
)
