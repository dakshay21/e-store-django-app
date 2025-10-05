#!/bin/bash

# Exit on any error
set -e

echo "Starting Django application..."

# Wait for database to be ready
echo "Waiting for database..."
echo "Trying to connect to $DB_HOST:$DB_PORT as user $DB_USER"
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "Database is unavailable - sleeping"
  sleep 1
done

echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Populate initial data
echo "Populating initial data..."
python manage.py populate_data

# Start the application
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
