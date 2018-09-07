

from rest_framework.test import APITestCase

from modeling.models import System, SurrogateModel, InputVariable, OutputVariable, DataSet
from modeling.analysis import train_initial_surrogate, update_surrogate

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

        # f1 = x^2
        # f2 = 3x - 1
        # n_sites = 11
        # x1 bounds = (-5., 4.)
        # x2 bounds = (-.5, 0.3)
        dataset_data = {
            'inputs': [{
                'name': 'x1',
                'values': [-5., -4.1, -3.2, -2.3, -1.4, -0.5, 0.4, 1.3, 2.2, 3.1, 4.]
            }, {
                'name': 'x2',
                'values': [-0.5, -0.42, -0.34, -0.26, -0.18, -0.1, -0.02, 0.06, 0.14, 0.22, 0.3]
            }],
            'outputs': [{
                'name': 'f1',
                'values': [25.0, 16.81, 10.24, 5.29, 1.96, 0.25, 0.16, 1.69, 4.84, 9.61, 16.0]
            }, {
                'name': 'f2',
                'values': [-2.5, -2.26, -2.02, -1.78, -1.54, -1.30, -1.06, -0.82, -0.58, -0.34, -0.10]
            }]
        }

        update_data = {
            'inputs': [{
                'name': 'x1',
                'values': [-0.5349978, 3.88431693, -3.21838491, 0.38599026]
            }, {
                'name': 'x2',
                'values': [0.24225488, -0.05801053, 0.26955379, -0.24816191]
            }],
            'outputs': [{
                'name': 'f1',
                'values': [0.286222, 15.087917, 10.358001, 0.148988]
            }, {
                'name': 'f2',
                'values': [-0.273235, -1.174031, -0.191338, -1.744485]
            }]
        }

        self.dataset = DataSet.objects.create(
            description='test dataset',
            data=dataset_data,
            system_id=self.system.id,
            runs=11
        )

        self.adaption_dataset = DataSet.objects.create(
            description='adaption dataset',
            data=update_data,
            runs=4
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

    def test_train_adapt_surrogate(self):
        system = System.objects.all()[0]
        dataset_train = DataSet.objects.all()[0]
        dataset_adapt = DataSet.objects.all()[1]

        train_initial_surrogate(system, dataset_train)
        update_surrogate(system, dataset_adapt)





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
