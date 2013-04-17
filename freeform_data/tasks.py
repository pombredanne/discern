"""
Used by celery to decide what tasks it needs to do
"""

from celery import task
import logging
from celery.task import periodic_task
from datetime import timedelta
from django.conf import settings
from django.core.management import call_command

log = logging.getLogger(__name__)

@periodic_task(run_every=timedelta(seconds=settings.TIME_BETWEEN_INDEX_REBUILDS))
def create_ml_models():
    call_command('rebuild_index', interactive=False)