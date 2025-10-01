#!/bin/zsh

echo "Checking for virtual environment..."

# Check if .venv directory exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating .venv with Python 3.12..."
    python3.12 -m venv .venv

    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment with python3.12"
        echo "Trying with python3..."
        python3 -m venv .venv

        if [ $? -ne 0 ]; then
            echo "Error: Failed to create virtual environment"
            exit 1
        fi
    fi

    echo "Virtual environment created successfully"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
source .venv/bin/activate

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "uv not found. Installing uv..."
    pip install uv
fi

# Install dependencies using uv
echo "Installing dependencies from requirements.txt..."
uv pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: uv pip install failed"
    exit 1
fi

echo "Dependencies installed successfully"
