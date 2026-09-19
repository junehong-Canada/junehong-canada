@echo off
setlocal

REM Switch to the directory where this script is located to ensure relative paths work
cd /d "%~dp0"

REM Check if Python is available in the PATH
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in the system PATH.
    exit /b 1
)

REM Install necessary Python libraries if they are missing
echo [INFO] Ensuring dependencies are installed...
pip install markdown pyyaml >nul

REM Execute the Python build script
echo [INFO] Building all blog posts...
python build_post.py

REM Generate blog index
echo [INFO] Updating blog index...
python update_blog_index.py

endlocal
