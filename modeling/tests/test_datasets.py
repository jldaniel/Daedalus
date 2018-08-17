
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from modeling.models import DataSet, System, InputVariable, OutputVariable


class TestCreateDataSet(APITestCase):

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

    def test_create_dataset(self):
        url = reverse('dataset-list', args=[self.system.id])
        data = {'description': 'test dataset',
                'data': {
                    'inputs': [{
                        'name': 'x1',
                        'values': [1.1, 2.3, -3.4, 5.9]
                    }, {
                        'name': 'x2',
                        'values': [-5.32, 9.13, 10.22, 3.23]
                    }],
                    'outputs': [{
                        'name': 'f1',
                        'values': [101.2, 42.1, -13.3, 5.55]
                    }, {
                        'name': 'f2',
                        'values': [0.12, 0.031, 1.99, 24.42]
                    }]}}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DataSet.objects.count(), 1)

        self.assertEqual(response.data['description'], data['description'])

    def test_missing_input(self):
        url = reverse('dataset-list', args=[self.system.id])
        data = {'description': 'test invalid dataset',
                'data': {
                    'inputs': [{
                        'name': 'x1',
                        'values': [1.1, 2.3, -3.4, 5.9]
                    }],
                    'outputs': [{
                        'name': 'f1',
                        'values': [101.2, 42.1, -13.3, 5.55]
                    }, {
                        'name': 'f2',
                        'values': [0.12, 0.031, 1.99, 24.42]
                    }]}}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("Incomplete dataset" in response.data)

    def test_create_invalid_input(self):
        url = reverse('dataset-list', args=[self.system.id])
        data = {'description': 'test invalid dataset',
                'data': {
                    'inputs': [{
                        'name': 'invalid',
                        'values': [1.1, 2.3, -3.4, 5.9]
                    }, {
                        'name': 'x2',
                        'values': [-5.32, 9.13, 10.22, 3.23]
                    }],
                    'outputs': [{
                        'name': 'f1',
                        'values': [101.2, 42.1, -13.3, 5.55]
                    }, {
                        'name': 'f2',
                        'values': [0.12, 0.031, 1.99, 24.42]
                    }]}}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("Unrecognized variable" in response.data)

    def test_missing_output(self):
        url = reverse('dataset-list', args=[self.system.id])
        data = {'description': 'test invalid dataset',
                'data': {
                    'inputs': [{
                        'name': 'x1',
                        'values': [1.1, 2.3, -3.4, 5.9]
                    }, {
                        'name': 'x2',
                        'values': [-5.32, 9.13, 10.22, 3.23]
                    }],
                    'outputs': [{
                        'name': 'f1',
                        'values': [101.2, 42.1, -13.3, 5.55]
                    }]}}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("Incomplete dataset" in response.data)

    def test_create_invalid_output(self):
        url = reverse('dataset-list', args=[self.system.id])
        data = {'description': 'test invalid dataset',
                'data': {
                    'inputs': [{
                        'name': 'x1',
                        'values': [1.1, 2.3, -3.4, 5.9]
                    }, {
                        'name': 'x2',
                        'values': [-5.32, 9.13, 10.22, 3.23]
                    }],
                    'outputs': [{
                        'name': 'f1',
                        'values': [101.2, 42.1, -13.3, 5.55]
                    }, {
                        'name': 'invalid',
                        'values': [0.12, 0.031, 1.99, 24.42]
                    }]}}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("Unrecognized variable" in response.data)

class TestGetDataSet(APITestCase):

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

        dataset_data = {
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
                'values': [03.45, 6.78, 3.33]

            }]}

        self.dataset = DataSet.objects.create(
            description='test dataset description',
            data=dataset_data,
            system_id=self.system.id
        )

        self.system.datasets.add(self.dataset)

    def test_get_dataset(self):
        url = reverse('dataset-detail', args=[self.dataset.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetDataSetList(APITestCase):

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

        self.dataset1 = DataSet.objects.create(
            description='test dataset description 2',
            data=dataset1_data,
            system_id=self.system.id
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

        self.dataset2 = DataSet.objects.create(
            description='test dataset description 2',
            data=dataset2_data,
            system_id=self.system.id
        )

        self.system.datasets.add(self.dataset1, self.dataset2)

    def test_get_dataset_list(self):
        url = reverse('dataset-list', args=[self.system.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class TestDeleteDataSet(APITestCase):
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

        self.dataset1 = DataSet.objects.create(
            description='test dataset description 2',
            data=dataset1_data,
            system_id=self.system.id
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

        self.dataset2 = DataSet.objects.create(
            description='test dataset description 2',
            data=dataset2_data,
            system_id=self.system.id
        )

        self.system.datasets.add(self.dataset1, self.dataset2)

    def test_delete_dataset(self):
        url = reverse('dataset-detail', args=[self.dataset1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        datasets = DataSet.objects.all()
        self.assertEqual(len(datasets), 1)
