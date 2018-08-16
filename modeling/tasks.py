from __future__ import absolute_import, unicode_literals
from celery import Celery, shared_task
from celery.utils.log import get_task_logger
from django.forms.models import model_to_dict
from django.conf import settings
import os

from daedalus.celery import app as celery

from modeling.analysis import SurrogateModel

app = Celery('modeling')

logger = get_task_logger(__name__)


@celery.task(name='modeling.tasks.train_surrogate')
def train_surrogate(system_id):
    surrogate = SurrogateModel()
    logger.info('test task called')

