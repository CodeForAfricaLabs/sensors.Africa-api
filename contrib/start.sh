#!/bin/sh
python manage.py migrate --noinput                # Apply database migrations
python manage.py collectstatic --clear --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /src/logs/celery.log
touch /src/logs/gunicorn.log
touch /src/logs/access.log
tail -n 0 -f /src/logs/*.log &

celery -A sensorsafrica beat -l info &> /src/log/celery.log  &
celery -A sensorsafrica worker -l info &> /src/log/celery.log  &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class gevent \
    --log-level=info \
    --log-file=/src/logs/gunicorn.log \
    --access-logfile=/src/logs/access.log \
    --name sensorsafrica --reload sensorsafrica.wsgi:application \
    --chdir sensorsafrica/
