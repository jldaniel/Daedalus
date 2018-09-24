from __future__ import absolute_import, unicode_literals
from celery import Celery, shared_task
from celery.utils.log import get_task_logger
from django.forms.models import model_to_dict
from django.conf import settings
from modeling.models import System, DataSet
from modeling.analysis import train_initial_surrogate, update_surrogate

from daedalus.celery import app as celery


app = Celery('modeling')

logger = get_task_logger(__name__)


@celery.task(name='modeling.tasks.train_surrogate')
def train_surrogate(system_id):

    # Get the system
    system = System.objects.get(pk=system_id)

    # Get the first dataset
    datasets = system.datasets.all()
    dataset = datasets[0]

    train_initial_surrogate(system, dataset)
    system.save()


@celery.task(name='modeling.tasks.update_surrogate')
def update_surrogate(system_id, dataset_id):
    system = System.objects.get(pk=system_id)
    dataset = DataSet.objects.get(pk=dataset_id)
    update_surrogate(system, dataset)
    system.status = 'READY'
    system.save()


