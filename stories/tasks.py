from __future__ import absolute_import, unicode_literals
from celery import shared_task
import datetime

from django.utils import timezone

from stories.models import Story


@shared_task(name="delete_expired_stories")
def delete_expired_stories(*args, **kwargs):
    date_time_before_24_hours = timezone.now() - datetime.timedelta(hours=24)
    Story.objects.filter(created_date__lt=date_time_before_24_hours).delete()

@shared_task(name="print_time")
def print_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Current Time is {current_time}")


@shared_task(name='get_calculation')
def calculate(val1, val2):
    total = val1 + val2
    return total