

from rest_framework.test import APITestCase

from modeling.models import System, SurrogateModel, InputVariable, OutputVariable, DataSet
from modeling.analysis import train_initial_surrogate

from django.conf import settings
import os

class TestAddSurrogate(APITestCase):

    def setUp(self):
        self.system = System.objects.create(name='test system', description='test description')

    def test_add_surrogate(self):
        surrogate = SurrogateModel.objects.create(system_id=self.system.id)

        self.assertEqual(SurrogateModel.objects.count(), 1)


class TestTrainSurrogate(APITestCase):

    def setUp(self):
        self.system = System.objects.create(name='test system', description='test description')
        self.x1 = InputVariable.objects.create(
            name='x1',
            description='x1 description',
            system_id=self.system.id
        )

        self.x2 = InputVariable.objects.create(
            name='x2',
            description='x2 description',
            system_id=self.system.id
        )

        self.system.input_variables.add(self.x1, self.x2)

        self.f1 = OutputVariable.objects.create(
            name='f1',
            description='f1 description',
            system_id=self.system.id
        )

        self.f2 = OutputVariable.objects.create(
            name='f2',
            description='f2 description',
            system_id=self.system.id
        )

        self.system.output_variables.add(self.f1, self.f2)

        dataset_data = {
            'inputs': [{
                'name': 'x1',
                'values': [-5., -4., -3., -2., -1.,  0.,  1.,  2.,  3.,  4.]
            }, {
                'name': 'x2',
                'values': [0., 0.22222222, 0.44444444, 0.66666667, 0.88888889, 1.11111111,
                           1.33333333, 1.55555556, 1.77777778, 2.]
            }],
            'outputs': [{
                'name': 'f1',
                'values': [25., 16.,  9.,  4.,  1.,  0.,  1.,  4.,  9., 16.]
            }, {
                'name': 'f2',
                'values': [-15.5, -12.5, -9.5, -6.5, -3.5, -0.5, 2.5, 5.5, 8.5, 11.5]
            }]
        }

        self.dataset = DataSet.objects.create(
            description='test dataset',
            data=dataset_data,
            system_id=self.system.id,
            runs=10
        )

    def test_train_surrogate(self):
        system = System.objects.all()[0]
        dataset = DataSet.objects.all()[0]

        train_initial_surrogate(system, dataset)

        self.assertTrue(system.surrogate is not None)
        self.assertTrue(os.path.exists(settings.SURROGATES_ROOT))

        surrogate = SurrogateModel.objects.all()[0]
        surrogate_path = surrogate.location
        self.assertTrue(os.path.isfile(surrogate_path))



class TestPredict(APITestCase):

    def setUp(self):
        self.system = System.objects.create(name='test system', description='test system description')
        self.x1 = InputVariable.objects.create(
            name='x1',
            description='x1 description',
            system_id=self.system.id)

        self.x2 = InputVariable.objects.create(
            name='x2',
            description='x2 description',
            system_id=self.system.id)

        self.system.input_variables.add(self.x1, self.x2)

        self.f1 = OutputVariable.objects.create(
            name='f1',
            description='f1 description',
            system_id=self.system.id
        )

        self.f2 = OutputVariable.objects.create(
            name='f2',
            description='f2 description',
            system_id=self.system.id
        )

        self.system.output_variables.add(self.f1, self.f2)
