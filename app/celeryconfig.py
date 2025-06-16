from celery.schedules import crontab

beat_schedule = {
    "check-expiring-notes-every-6-hours": {
        "task": "app.utils.tasks.notify_and_cleanup_notes",
        "schedule": crontab(minute=0, hour="*/6"),
    },
    "refresh-redis-cache-every-10-mins": {
        "task": "app.utils.tasks.refresh_recent_notes_cache",
        "schedule": crontab(minute="*/10"),
    },
}
timezone = "UTC"
