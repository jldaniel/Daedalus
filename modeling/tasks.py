from __future__ import absolute_import, unicode_literals
from celery import Celery, shared_task
from celery.utils.log import get_task_logger
from django.forms.models import model_to_dict
from django.conf import settings
from modeling.models import System
import os

from daedalus.celery import app as celery

from kaolin import Surrogate

app = Celery('modeling')

logger = get_task_logger(__name__)


@celery.task(name='modeling.tasks.train_surrogate')
def train_surrogate(system_id):

    # Get the system
    system = System.objects.get(pk=system_id)

    surrogate = Surrogate()
    logger.info('test task called')

