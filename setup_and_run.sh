#!/bin/bash

# Script to set up the environment and run the Streamlit application
echo "Setting up Report Tools environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python 3.8+ to continue."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run the Streamlit application
echo "Starting Streamlit application..."
streamlit run app.py

# Deactivate virtual environment on exit
deactivate
