web: gunicorn subwayapi.wsgi
worker: celery -A subwayapi beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler