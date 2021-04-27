web: gunicorn subwayapi.wsgi
worker: celery -A subwayapi beat -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler