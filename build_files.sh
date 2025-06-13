#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput --clear

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles_build

# Copy static files to the build directory
cp -r staticfiles/* staticfiles_build/ 