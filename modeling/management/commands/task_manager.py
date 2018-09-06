from django.core.management.base import BaseCommand, CommandError
from modeling.models import System
from multiprocessing import Process
import time
from modeling.tasks import train_surrogate, update_surrogate
from modeling.models import SYSTEM_STATUS

# Sets up the manager thread
# python manage.py task_manager


def check_system_status():
    while True:
        systems = System.objects.all()
        for system in systems:
            print('Checking system', system.name, ':', system.id)
            status = system.status

            if status == 'CREATED':
                # Check if any datasets have been applied
                if system.datasets:
                    system.status = 'BUSY'
                    train_surrogate.apply_async(args=[system.id])

            elif status == 'READY':
                dataset_ids = []
                # TODO This can be handled by a query
                for dataset in system.datasets.all():
                    if not dataset.applied:
                        dataset_ids.append(dataset.id)

                if dataset_ids:
                    system.status = 'BUSY'
                    update_surrogate.apply_async(args=[system.id, dataset_ids])

            elif status == 'BUSY' or status == 'ERROR':
                pass

            time.sleep(2)




class Command(BaseCommand):
    help = 'Starts the Daedalus task manager'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting system manager process...'))
        p = Process(target=check_system_status)
        p.start()
