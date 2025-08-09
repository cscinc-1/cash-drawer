#!/bin/bash

# Copy database file if it doesn't exist in /data and exists in project
if [ ! -f /data/BullittDrawer.db ] && [ -f /app/BullittDrawer.db ]; then
    echo "Copying database file to /data/..."
    cp /app/BullittDrawer.db /data/BullittDrawer.db
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start server based on environment
if [ "$DEBUG" = "true" ] || [ "$DJANGO_DEBUG" = "true" ] || [ "$ENV" = "development" ]; then
    echo "Starting Django development server..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "Starting Gunicorn..."
    exec gunicorn cashdrawer_reports.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --threads 2 \
        --worker-class gthread \
        --timeout 120 \
        --access-logfile - \
        --error-logfile -
fi