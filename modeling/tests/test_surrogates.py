

from rest_framework.test import APITestCase

from modeling.models import System, SurrogateModel, InputVariable, OutputVariable, DataSet


class TestAddSurrogate(APITestCase):

    def setUp(self):
        self.system = System.objects.create(name='test system', description='test description')

    def test_add_surrogate(self):
        surrogate = SurrogateModel.objects.create(system_id=self.system.id)

        self.assertEqual(SurrogateModel.objects.count(), 1)


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
