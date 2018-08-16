

from rest_framework.test import APITestCase

from modeling.models import System, Surrogate


class TestAddSurrogate(APITestCase):

    def setUp(self):
        self.system = System.objects.create(name='test system', description='test description')

    def test_add_surrogate(self):
        surrogate = Surrogate.objects.create(system_id=self.system.id)

        self.assertEqual(Surrogate.objects.count(), 1)



