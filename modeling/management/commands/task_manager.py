from django.core.management.base import BaseCommand, CommandError
from modeling.models import System
from multiprocessing import Process
import time
from modeling.tasks import train_surrogate
from modeling.models import SYSTEM_STATUS

# Sets up the manager thread
# python manage.py task_manager


def check_system_status():
    while True:
        systems = System.objects.all()
        for system in systems:
            print('Checking system ' + str(system.id))
            status = system.status

            if status == 'READY':
                # Kick off an asynch process to start training the system
                system.status = 'TRAINING'
                system.save()
                train_surrogate.apply_async(args=[system.id])

            elif status == 'TRAINING':
                # Check that the system is actually training, if not set the status to ready
                pass

            elif status == 'IDLE':
                # do nothing?
                pass

            elif status == 'ERROR':
                # pass
                pass

            else:
                print('Unknown status ' + str(status))

            time.sleep(5)


class Command(BaseCommand):
    help = 'Starts the Daedalus task manager'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting system manager process...'))
        p = Process(target=check_system_status)
        p.start()
