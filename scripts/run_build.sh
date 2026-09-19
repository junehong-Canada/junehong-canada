#!/bin/bash

# Switch to the directory where this script is located to ensure relative paths work
cd "$(dirname "$0")"

# Check if Python is available
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "[ERROR] Python is not installed or not in the system PATH."
    exit 1
fi

# Install necessary Python libraries if they are missing
echo "[INFO] Ensuring dependencies are installed..."
$PYTHON_CMD -m pip install markdown pyyaml >/dev/null

# Execute the Python build script
echo "[INFO] Building all blog posts..."
$PYTHON_CMD build_post.py

# Generate blog index
echo "[INFO] Updating blog index..."
$PYTHON_CMD update_blog_index.py