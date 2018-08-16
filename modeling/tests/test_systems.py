
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from modeling.models import InputVariable, OutputVariable, System, SYSTEM_STATUS

valid_system_data = {'name': 'system with vars',
                     'description': 'system with vars description',
                     'input_variables': [
                         {'name': 'x1',
                          'description': 'x1 var description',
                          'lower_bound': 1.2,
                          'upper_bound': 5.4},
                         {'name': 'x2',
                          'description': 'x2 var description',
                          'lower_bound': -3.24,
                          'upper_bound': 0.0}],
                     'output_variables': [
                         {'name': 'f1',
                          'description': 'f1 var description'},
                         {'name': 'f2',
                          'description': 'f2 var description'}]
                     }


class TestCreateSystem(APITestCase):

    def test_create_system(self):
        url = reverse('system-list')
        data = {'name': 'system with vars',
                'description': 'system with vars description',
                'input_variables': [
                    {'name': 'x1',
                     'description': 'x1 var description',
                     'lower_bound': 1.2,
                     'upper_bound': 5.4},
                    {'name': 'x2',
                     'description': 'x2 var description',
                     'lower_bound': -3.24,
                     'upper_bound': 0.0}],
                'output_variables': [
                    {'name': 'f1',
                     'description': 'f1 var description'},
                    {'name': 'f2',
                     'description': 'f2 var description'}]
                }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(System.objects.count(), 1)

        system = System.objects.get()

        self.assertEqual(system.name, data['name'])
        self.assertEqual(system.description, data['description'])
        self.assertEqual(system.status, SYSTEM_STATUS[0][0])

        x1 = system.input_variables.get(name='x1')
        self.assertEqual(x1.name, data['input_variables'][0]['name'])
        self.assertEqual(x1.description, data['input_variables'][0]['description'])
        self.assertEqual(x1.lower_bound, data['input_variables'][0]['lower_bound'])
        self.assertEqual(x1.upper_bound, data['input_variables'][0]['upper_bound'])

        x2 = system.input_variables.get(name='x2')
        self.assertEqual(x2.name, data['input_variables'][1]['name'])
        self.assertEqual(x2.description, data['input_variables'][1]['description'])
        self.assertEqual(x2.lower_bound, data['input_variables'][1]['lower_bound'])
        self.assertEqual(x2.upper_bound, data['input_variables'][1]['upper_bound'])

        f1 = system.output_variables.get(name='f1')
        self.assertEqual(f1.name, data['output_variables'][0]['name'])
        self.assertEqual(f1.description, data['output_variables'][0]['description'])

        f2 = system.output_variables.get(name='f2')
        self.assertEqual(f2.name, data['output_variables'][1]['name'])
        self.assertEqual(f2.description, data['output_variables'][1]['description'])


class TestGetSystem(APITestCase):

    system_name = 'test system'
    system_description = 'test description'
    system_status = SYSTEM_STATUS[0][0]

    def setUp(self):
        self.system = System.objects.create(name=self.system_name, description=self.system_description)
        self.x1 = InputVariable.objects.create(
            name='x1',
            description='x1 description',
            system_id=self.system.id,
            lower_bound=0.0,
            upper_bound=1.0)

        self.x2 = InputVariable.objects.create(
            name='x2',
            description='x2 description',
            system_id=self.system.id,
            lower_bound=0.0,
            upper_bound=1.0)

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

    def test_get_system(self):
        url = reverse('system-detail', args=[self.system.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.system_name)
        self.assertEqual(response.data['description'], self.system_description)
        self.assertEqual(response.data['status'], self.system_status)
        self.assertTrue('created' in response.data)
        self.assertTrue('updated' in response.data)

        self.assertEqual(len(response.data['input_variables']), 2)
        self.assertEqual(len(response.data['output_variables']), 2)

        x1 = [var for var in response.data['input_variables'] if var['name'] == 'x1'][0]
        self.assertEqual(x1['name'], self.x1.name)
        self.assertEqual(x1['description'], self.x1.description)
        self.assertEqual(x1['lower_bound'], self.x1.lower_bound)
        self.assertEqual(x1['upper_bound'], self.x1.upper_bound)

        x2 = [var for var in response.data['input_variables'] if var['name'] == 'x2'][0]
        self.assertEqual(x2['name'], self.x2.name)
        self.assertEqual(x2['description'], self.x2.description)
        self.assertEqual(x2['lower_bound'], self.x2.lower_bound)
        self.assertEqual(x2['upper_bound'], self.x2.upper_bound)

        f1 = [var for var in response.data['output_variables'] if var['name'] == 'f1'][0]
        self.assertEqual(f1['name'], self.f1.name)
        self.assertEqual(f1['description'], self.f1.description)

        f2 = [var for var in response.data['output_variables'] if var['name'] == 'f2'][0]
        self.assertEqual(f2['name'], self.f2.name)
        self.assertEqual(f2['description'], self.f2.description)


class TestGetSystemList(APITestCase):
    system_name_1 = 'test system 1'
    system_description_1 = 'test description 1'

    system_name_2 = 'test system 2'
    system_description_2 = 'test description 2'

    def setUp(self):
        self.system_1 = System.objects.create(name=self.system_name_1, description=self.system_description_1)
        self.system_2 = System.objects.create(name=self.system_name_2, description=self.system_description_2)

    def test_get_system_list(self):
        url = reverse('system-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.system_name_1)
        self.assertEqual(response.data[0]['description'], self.system_description_1)
        self.assertEqual(response.data[1]['name'], self.system_name_2)
        self.assertEqual(response.data[1]['description'], self.system_description_2)


class TestUpdateSystem(APITestCase):
    system_name = 'test system'
    system_description = 'test description'

    update_name_data = {'name': 'updated system'}
    update_description_data = {'description': 'updated description'}

    def setUp(self):
        self.system = System.objects.create(name=self.system_name, description=self.system_description)

    def test_update_name(self):
        url = reverse('system-detail', args=[self.system.id])
        response = self.client.put(url, data=self.update_name_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.update_name_data['name'])

    def test_update_description(self):
        url = reverse('system-detail', args=[self.system.id])
        response = self.client.put(url, data=self.update_description_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.update_description_data['description'])


class TestDeleteSystem(APITestCase):
    system_name = 'test system'
    system_description = 'test description'

    def setUp(self):
        self.system = System.objects.create(name=self.system_name, description=self.system_description)

    def test_delete_system(self):
        url = reverse('system-detail', args=[self.system.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

