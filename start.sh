#!/bin/bash

# Railway Startup Script
# This script runs migrations and seeding before starting the app

echo "🚀 Starting Railway deployment..."

# Run database migrations
echo "📦 Running database migrations..."
flask db upgrade

# Check if migration was successful
if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migration failed!"
    exit 1
fi

# Seed the database (only if empty)
echo "🌱 Seeding database..."
python seed_db.py

# Start the application with Gunicorn
echo "🎯 Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 app:app
