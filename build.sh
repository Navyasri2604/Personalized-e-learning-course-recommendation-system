#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate

echo "==> Seeding database with courses..."
python manage.py seed_data

echo "==> Build complete!"
