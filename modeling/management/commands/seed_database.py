from django.core.management.base import BaseCommand
from modeling.models import System, InputVariable, OutputVariable, DataSet


class Command(BaseCommand):
    help = 'Seeds the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding the database...'))

        system = System.objects.create(name='test system', description='test system description')
        x1 = InputVariable.objects.create(
            name='x1',
            description='x1 description',
            system_id=system.id)

        x2 = InputVariable.objects.create(
            name='x2',
            description='x2 description',
            system_id=system.id)

        system.input_variables.add(x1, x2)

        f1 = OutputVariable.objects.create(
            name='f1',
            description='f1 description',
            system_id=system.id
        )

        f2 = OutputVariable.objects.create(
            name='f2',
            description='f2 description',
            system_id=system.id
        )

        system.output_variables.add(f1, f2)

        dataset1_data = {
            'inputs': [{
                'name': 'x1',
                'values': [1.23, 9.01, 0.12]
            }, {
                'name': 'x2',
                'values': [5.63, 7.23, 0.01]
            }],
            'outputs': [{
                'name': 'f1',
                'values': [0.23, 4.34, 8.13]
            }, {
                'name': 'f2',
                'values': [3.45, 6.78, 3.33]

            }]}

        dataset1 = DataSet.objects.create(
            description='test dataset description 2',
            data=dataset1_data,
            system_id=system.id
        )

        dataset2_data = {
            'inputs': [{
                'name': 'x1',
                'values': [11.23, 19.01, 20.12]
            }, {
                'name': 'x2',
                'values': [35.63, 47.23, 50.01]
            }],
            'outputs': [{
                'name': 'f1',
                'values': [60.23, 74.34, 88.13]
            }, {
                'name': 'f2',
                'values': [3.45, 6.78, 93.33]

            }]}

        dataset2 = DataSet.objects.create(
            description='test dataset description 2',
            data=dataset2_data,
            system_id=system.id
        )

        system.datasets.add(dataset1, dataset2)

        # System 2
        system = System.objects.create(name='Satellite', description='Complex satellite model')
        x1 = InputVariable.objects.create(
            name='x1',
            description='x1 description',
            system_id=system.id)

        x2 = InputVariable.objects.create(
            name='x2',
            description='x2 description',
            system_id=system.id)

        system.input_variables.add(x1, x2)

        f1 = OutputVariable.objects.create(
            name='f1',
            description='f1 description',
            system_id=system.id
        )
        system.output_variables.add(f1)

        self.stdout.write(self.style.SUCCESS('Database seeded'))
