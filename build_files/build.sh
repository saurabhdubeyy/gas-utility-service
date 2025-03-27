#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Try to create default support user if none exists, but don't fail the build if it errors
echo "Attempting to create default support user..."
python manage.py create_support_user || echo "Support user creation skipped or failed (this is not critical)" 