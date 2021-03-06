import os

from celery import Celery
from celery_slack import Slackify

# Set sensorsafrica application settings module for sensorsafrica Celery instance
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensorsafrica.settings")

# Create Celery instance and pass the project name
# The instance is bound to the variable app
app = Celery("sensorsafrica")

# Pass config made of up values begging with the prefix of CELERY_ in settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks in tasks.py
app.autodiscover_tasks()

SLACK_WEBHOOK = os.environ.get("SENSORSAFRICA_CELERY_SLACK_WEBHOOK", "")
SLACK_WEBHOOK_FAILURES_ONLY = os.environ.get(
    "SENSORSAFRICA_CELERY_SLACK_WEBHOOK_FAILURES_ONLY", "").strip().lower() in ('true', 't', '1')

options = {'failures_only': SLACK_WEBHOOK_FAILURES_ONLY}

slack_app = Slackify(app, SLACK_WEBHOOK, **options)
