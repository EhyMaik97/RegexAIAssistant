import os
import sys
import subprocess
import shutil

def build_exe():
    print("Building executable file for Regex AI Assistant...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"Found PyInstaller version {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Install all dependencies from requirements.txt
    print("Installing dependencies from requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Clean previous builds if they exist
    if os.path.exists("dist"):
        print("Cleaning previous builds...")
        shutil.rmtree("dist", ignore_errors=True)
    if os.path.exists("build"):
        shutil.rmtree("build", ignore_errors=True)
    if os.path.exists("RegexAIAssistant.spec"):
        os.remove("RegexAIAssistant.spec")
    
    # Check if .env file exists, create if not
    if not os.path.exists(".env"):
        print("Creating .env file for API key...")
        with open(".env", "w") as f:
            f.write("GROQ_API_KEY=your_api_key_here\n")
        print("Please edit .env file and add your actual GROQ API key before running the application")
    
    # Check if icon directory exists, create if not
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # Check if icon file exists, create a default one if not
    icon_path = "assets/app_icon.ico"
    if not os.path.exists(icon_path):
        print("Creating a default icon file...")
        try:
            from PIL import Image, ImageDraw
            
            # Create a simple icon
            img = Image.new('RGBA', (256, 256), color=(0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            
            # Draw a blue circle
            d.ellipse((20, 20, 236, 236), fill=(0, 120, 215))
            
            # Draw an "R" in white
            d.rectangle((80, 70, 180, 190), fill=(255, 255, 255))
            d.rectangle((100, 100, 170, 160), fill=(0, 120, 215))
            d.polygon([(170, 70), (180, 70), (180, 190), (140, 190), (140, 170), (160, 170), (160, 90), (130, 90), (130, 130), (150, 130), (150, 110), (170, 110)], fill=(0, 120, 215))
            
            # Save as .ico format
            img.save(icon_path)
            print(f"Default icon created at {icon_path}")
        except Exception as e:
            print(f"Failed to create default icon: {e}")
            print("You can add your own icon file at 'assets/app_icon.ico'")
            icon_path = None
    
    # Create a custom .spec file for PyInstaller with fixed formatting
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

a = Analysis(
    ['app/app.py'],
    pathex=[],
    binaries=[],
    datas=[('app/chains.py', 'app'), ('app/template.txt', 'app'), ('.env', '.'), ('assets', 'assets')],
    hiddenimports=[
        'langchain_groq', 
        'langchain_core', 
        'python_dotenv',
        'dotenv',
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'groq',
        'pydantic',
        'typing_extensions',
        'PIL',
        'langchain_core.prompts',
        'langchain_core.language_models',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add all dependencies from requirements.txt
import pkg_resources
try:
    # Read requirements file
    with open('requirements.txt', 'r') as req_file:
        for line in req_file:
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract package name
                pkg_name = line.split('==')[0].split('>=')[0].strip()
                try:
                    # Add the package
                    a.hiddenimports.append(pkg_name.replace('-', '_'))
                    # Add its dependencies
                    reqs = pkg_resources.get_distribution(pkg_name).requires()
                    if reqs:
                        for req in reqs:
                            a.hiddenimports.append(req.name.replace('-', '_'))
                except:
                    pass
except Exception as e:
    print(f"Error processing requirements: {e}")

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RegexAIAssistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None"""
    
    # Add icon if available - with no trailing comma
    if icon_path and os.path.exists(icon_path):
        spec_content += f",\n    icon='{icon_path}'"
    
    spec_content += "\n)"
    
    # Write the spec file
    with open("RegexAIAssistant.spec", "w") as spec_file:
        spec_file.write(spec_content)
    
    # Build using the spec file
    print("Building the executable...")
    subprocess.call(["pyinstaller", "RegexAIAssistant.spec"])
    
    print("\nBuild complete!")
    print("Executable created at: dist/RegexAIAssistant.exe")
    print("You can now distribute this file to run the application without Python installed.")
    print("NOTE: The GROQ API key must be set in the environment or in a .env file in the same directory as the executable.")

if __name__ == "__main__":
    build_exe() 