import os
import platform
import subprocess
import shutil
import sys
from pathlib import Path
import urllib.parse

def check_requirements():
    """Check if all required files exist"""
    # List of possible model filenames (including URL-encoded version)
    model_filenames = [
        's2a-q4-hq-fast-en+pl.model',
        's2a-q4-hq-fast-en%2Bpl.model'
    ]
    
    required_files = ['server.py']
    
    # Check for model file with any of the possible names
    model_found = False
    for model_name in model_filenames:
        if os.path.exists(model_name):
            required_files.append(model_name)
            model_found = True
            break
    
    if not model_found:
        print("Error: Model file not found. Please ensure one of the following exists:")
        for model_name in model_filenames:
            print(f"  - {model_name}")
        sys.exit(1)
    
    # Check other required files
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Error: The following required files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nPlease ensure all required files are present before building.")
        sys.exit(1)

def clean_build():
    """Clean previous build artifacts"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    if os.path.exists('compiled_whisper.spec'):
        os.remove('compiled_whisper.spec')

def build_executable():
    """Build the executable using PyInstaller"""
    system = platform.system().lower()
    
    # Find the model file (check both possible names)
    model_file = None
    for model_name in ['s2a-q4-hq-fast-en+pl.model', 's2a-q4-hq-fast-en%2Bpl.model']:
        if os.path.exists(model_name):
            model_file = model_name
            break
    
    if not model_file:
        print("Error: Model file not found")
        sys.exit(1)
    
    # Base PyInstaller command
    cmd = [
        'pyinstaller',
        '--name=compiled_whisper',
        '--onefile',
        '--noconsole',  # Hide console window
        f'--add-data={model_file}:.',  # Include the model file
        'server.py'
    ]
    
    # Platform-specific configurations
    if system == 'darwin':  # macOS
        cmd.extend([
            '--codesign-identity=-',  # Skip code signing
            '--osx-entitlements-file=entitlements.plist'  # Add entitlements
        ])
    elif system == 'windows':
        cmd.extend([
            '--icon=icon.ico'  # Add Windows icon if available
        ])
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Error during PyInstaller build:")
            print(result.stderr)
            sys.exit(1)
        
        # Create platform-specific output directory
        output_dir = Path('dist') / f'compiled_whisper_{system}'
        output_dir.mkdir(exist_ok=True)
        
        # Copy executable to platform-specific directory
        if system == 'windows':
            exe_path = 'dist/compiled_whisper.exe'
        else:
            exe_path = 'dist/compiled_whisper'
            
        if not os.path.exists(exe_path):
            print(f"Error: Executable not found at {exe_path}")
            print("Build output:")
            print(result.stdout)
            sys.exit(1)
            
        shutil.copy(exe_path, output_dir / os.path.basename(exe_path))
        
        # Copy model file
        if os.path.exists(model_file):
            shutil.copy(model_file, output_dir / model_file)
        else:
            print(f"Warning: Model file {model_file} not found. Please copy it manually to {output_dir}")
        
        print(f"\nBuild completed successfully!")
        print(f"Executable location: {output_dir}")
        
    except Exception as e:
        print(f"Error during build process: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    print("Checking requirements...")
    check_requirements()
    
    print("Cleaning previous build...")
    clean_build()
    
    print("Building executable...")
    build_executable() 