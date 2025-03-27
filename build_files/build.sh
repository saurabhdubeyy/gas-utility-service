#!/bin/bash
# Build script for Render deployment

# Exit on error
set -o errexit

# Python version: 3.9.12
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!" 