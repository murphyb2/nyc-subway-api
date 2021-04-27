from __future__ import absolute_import, unicode_literals

from celery import shared_task

@shared_task
def add(x,y):
    print(f'adding {x} and {y}')
    return x + y