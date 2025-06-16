from celery.schedules import crontab

beat_schedule = {
    "check-expiring-notes-every-10-min": {
        "task": "app.utils.tasks.notify_expiring_notes",
        "schedule": crontab(minute=0, hour="*/6"),
    }
}

timezone = "UTC"
