import os
import shutil
import subprocess
import sys
import PyInstaller.__main__


def build_game():
    try:
        # Clean previous builds
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('build'):
            shutil.rmtree('build')

        # Get the Python executable path
        python_exe = sys.executable

        # Create game.spec if it doesn't exist
        if not os.path.exists('game.spec'):
            create_spec_file()

        print("Building game...")
        # Build the game using Python's executable
        result = subprocess.run(
            [python_exe, '-m', 'PyInstaller', 'game.spec', '--clean'],
            text=True
        )  # Removed capture_output=True to see the output

        if result.returncode != 0:
            print("Build failed")
            return

        print("Creating itch.io files...")
        # Create itch.io specific files
        create_html_launcher()
        create_itch_metadata()

        print("Creating ZIP file...")
        # Create ZIP file
        if os.path.exists('dist'):  # Changed from 'dist/SquareShooter'
            shutil.make_archive('SquareShooter-Windows', 'zip', 'dist')
            print("Build completed successfully!")
        else:
            print("Error: Build directory not found")

    except Exception as e:
        print(f"An error occurred: {e}")

def create_spec_file():
    """Create the PyInstaller spec file"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Get the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))

a = Analysis(
    ['main.py'],  # Your main game file
    pathex=[current_dir],
    binaries=[],
    datas=[
        ('assets', 'assets'),  # Include all assets
        ('config', 'config'),  # Include config files
    ],
    hiddenimports=['pygame'],
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
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/game_icon.ico' if os.path.exists('assets/icons/game_icon.ico') else None
)"""

    with open('game.spec', 'w') as f:
        f.write(spec_content)


def create_html_launcher():
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Square Shooter</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #000;
            color: #fff;
            font-family: Arial, sans-serif;
        }
        .launch-container {
            text-align: center;
        }
        .download-button {
            display: inline-block;
            padding: 15px 30px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="launch-container">
        <h1>Square Shooter</h1>
        <p>Download and run the game to play!</p>
        <a href="SquareShooter-Windows.zip" class="download-button">Download Game</a>
    </div>
</body>
</html>
"""
    os.makedirs('dist', exist_ok=True)
    with open('dist/index.html', 'w') as f:
        f.write(html_content)


def create_itch_metadata():
    metadata = """[build]
directory = "SquareShooter-Windows"
[package]
name = "square-shooter"
version = "1.0.0"
authors = ["Your Name"]
"""
    with open('dist/.itch.toml', 'w') as f:
        f.write(metadata)


def build_web_version():
    """Build web version using pygbag"""
    try:
        print("Building web version...")
        # Create web directory
        if os.path.exists('web'):
            shutil.rmtree('web')
        os.makedirs('web')

        # Copy your game files to web directory
        directories_to_copy = ['core', 'config', 'entities', 'utils', 'ui', 'visual', 'assets']
        for directory in directories_to_copy:
            if os.path.exists(directory):
                shutil.copytree(directory, f'web/{directory}')

        # Copy main.py to web directory
        shutil.copy2('main.py', 'web/main.py')

        # Run pygbag
        subprocess.run([
            sys.executable,
            '-m',
            'pygbag',
            '--app-name=SquareShooter',
            '--ume_block=0',
            '--can_close=1',
            '--cache=1',
            '--bind=0.0.0.0',
            'web'
        ])

        print("Web build completed!")

        # Create web zip for itch.io
        if os.path.exists('build/web'):
            shutil.make_archive('SquareShooter-Web', 'zip', 'build/web')
            print("Web package created: SquareShooter-Web.zip")

    except Exception as e:
        print(f"Error building web version: {e}")


# Modify main to build both versions
if __name__ == '__main__':
    build_game()
    build_web_version()
