# Celery - Scheduled Task Updating

## In Production

In production, celery beat can be embedded into the worker. We only ever have one task running so this works fine as one process.

```shell
celery -A subwayapi worker -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## In Development

You can use the production command in development UNLESS you are running on a Windows machine. In which case celery beat needs to run in a separate service. Run the following commands in to terminal instances:

```shell
celery -A subwayapi beat -l INFO
```

```shell
celery -A subwayapi worker -l info --pool=solo
```
