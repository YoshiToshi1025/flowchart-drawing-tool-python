#!/bin/bash
cd "$(dirname "$0")" || exit 1

error() {
    echo "An error occurred."
    read -r -p "Press Enter to exit..."
    exit 1
}

# Check Python
if ! python3 --version; then
    echo "Please install Python first."
    read -r -p "Press Enter to exit..."
    exit 1
fi

# Create virtual environment
if [ ! -x "env/bin/python" ]; then
    python3 -m venv env || error
fi

# Install required packages
env/bin/python -m pip install -r requirements.txt || error

# Start application
env/bin/python flowchart_tool.py || error
exit 0