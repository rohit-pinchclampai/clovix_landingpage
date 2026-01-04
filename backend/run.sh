#!/bin/bash

# Quick start script for the backend API

echo "Starting Clovix Backend API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the server
echo "Starting server on http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
python main.py

