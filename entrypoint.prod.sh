#!/bin/bash

# Exit on any error
set -e

echo "Starting Django application in production mode..."

# Wait for database to be ready (RDS)
echo "Waiting for database..."
echo "Trying to connect to $DB_HOST:$DB_PORT as user $DB_USER"
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; then
        echo "Database is ready!"
        break
    fi
    attempt=$((attempt + 1))
    echo "Database is unavailable - sleeping (attempt $attempt/$max_attempts)"
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "ERROR: Could not connect to database after $max_attempts attempts"
    exit 1
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Only populate data if POPULATE_DATA environment variable is set
if [ "${POPULATE_DATA:-false}" = "true" ]; then
    echo "Populating initial data..."
    python manage.py populate_data
else
    echo "Skipping data population (set POPULATE_DATA=true to enable)"
fi

# Start the application with Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn ecommerce_backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-4} \
    --worker-class sync \
    --timeout ${GUNICORN_TIMEOUT:-30} \
    --keep-alive 2 \
    --max-requests ${GUNICORN_MAX_REQUESTS:-1000} \
    --max-requests-jitter ${GUNICORN_MAX_REQUESTS_JITTER:-50} \
    --access-logfile - \
    --error-logfile - \
    --log-level ${LOG_LEVEL:-info}
