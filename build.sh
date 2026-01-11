#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip to latest version
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --no-input --clear

# Run database migrations
python3 manage.py migrate
