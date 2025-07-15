# -*- mode: python ; coding: utf-8 -*-
import os

from PyInstaller.building.api import PYZ, EXE
from PyInstaller.building.build_main import Analysis
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Get the current directory
current_dir = os.getcwd()

a = Analysis(
    ['src/main.py'],  # Main game file in src folder
    pathex=[current_dir],
    binaries=[],
    datas=[
        ('assets/images', 'assets/images'),
        ('assets/audio', 'assets/audio'),
        ('src/config', 'config'),
        ('src/entities', 'entities'),
        ('src/utils', 'utils'),
        ('src/ui', 'ui'),
        ('src/core', 'core'),
        ('src/visual', 'visual')
    ],
    hiddenimports=[
        'pygame',
        'random',
        'math',
        'enum'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SquareShooter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep True for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Temporarily removed icon
)
