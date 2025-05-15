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
    
    # Ensure required dependencies are installed
    dependencies = ["langchain-groq", "python-dotenv"]
    for dep in dependencies:
        try:
            __import__(dep.replace("-", "_"))
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
    
    # Check if .env file exists, create if not
    if not os.path.exists(".env"):
        print("Creating .env file for API key...")
        with open(".env", "w") as f:
            f.write("GROQ_API_KEY=your_api_key_here\n")
        print("Please edit .env file and add your actual GROQ API key before running the application")
    
    # Create spec file and build the executable
    print("Creating executable...")
    
    # Determine the correct separator for --add-data based on platform
    separator = ";" if sys.platform.startswith("win") else ":"
    
    cmd = [
        "pyinstaller",
        "--name=RegexAIAssistant",
        "--noconsole",  # No console window
        "--onefile",    # Single file executable
        f"--add-data=app/chains.py{separator}app",  # Include the chains module
        f"--add-data=app/template.txt{separator}app",  # Include the template file
        f"--add-data=.env{separator}.",  # Include the .env file
        "--icon=NONE",  # Replace with your icon if you have one
        "app/app.py"
    ]
    
    subprocess.call(cmd)
    
    print("\nBuild complete!")
    print("Executable created at: dist/RegexAIAssistant.exe")
    print("You can now distribute this file to run the application without Python installed.")
    print("NOTE: The GROQ API key must be set in the environment or in a .env file in the same directory as the executable.")

if __name__ == "__main__":
    build_exe() 