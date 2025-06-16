from celery import Celery

celery_app = Celery(
    'fundoo_notes',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=['app.utils.tasks'],
    broker_connection_retry_on_startup=True
)
celery_app.config_from_object('app.celeryconfig')