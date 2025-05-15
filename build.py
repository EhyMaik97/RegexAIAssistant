import os
import sys
import subprocess
import shutil
import pkg_resources

def build_exe():
    print("Building executable file for Regex AI Assistant...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"Found PyInstaller version {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Ensure required dependencies are installed
    dependencies = ["langchain-groq", "python-dotenv", "langchain-core", "PyQt5"]
    for dep in dependencies:
        try:
            module_name = dep.replace("-", "_")
            __import__(module_name)
            print(f"Found {dep}")
        except ImportError:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
    
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
    
    # Create a custom .spec file for PyInstaller
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

a = Analysis(
    ['app/app.py'],
    pathex=[],
    binaries=[],
    datas=[('app/chains.py', 'app'), ('app/template.txt', 'app'), ('.env', '.')],
    hiddenimports=['langchain_groq', 'langchain_core', 'python_dotenv', 'dotenv', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],
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
for pkg in ['langchain-groq', 'langchain-core', 'python-dotenv', 'PyQt5']:
    try:
        reqs = pkg_resources.get_distribution(pkg).requires()
        if reqs:
            for req in reqs:
                a.hiddenimports.append(req.name)
    except:
        pass

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
    entitlements_file=None,
)
"""
    
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