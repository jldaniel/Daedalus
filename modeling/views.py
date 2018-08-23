from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from modeling.models import System, DataSet
from modeling.serializers import SystemSerializer, DataSetListSerializer, DataSetDetailsSerializer

import json


@api_view(['POST', 'GET'])
def system_list(request, format=None):
    if request.method == 'POST':
        serializer = SystemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        systems = System.objects.all()
        serializer = SystemSerializer(systems, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def system_detail(request, system_id, format=None):
    try:
        system = System.objects.get(pk=system_id)
    except System.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SystemSerializer(system)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SystemSerializer(system, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        system.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'GET'])
def dataset_list(request, system_id, format=None):
    if request.method == 'POST':
        try:
            system = System.objects.get(pk=system_id)
        except System.DoesNotExist:
            # TODO: Add in message as well to let the user know the specified system does not exist
            return Response("System with id: " + str(system_id) + " does not exist",
                                                     status=status.HTTP_400_BAD_REQUEST)

        # Validate the incoming data field
        data = request.data

        input_variable_names = [var.name for var in system.input_variables.all()]
        inputs = data['data']['inputs']

        if len(input_variable_names) != len(inputs):
            missing_inputs = [var['name'] for var in inputs if var['name'] not in input_variable_names]
            return Response("Incomplete dataset, missing data for input variables " +
                            repr(missing_inputs), status=status.HTTP_400_BAD_REQUEST)

        for input in inputs:
            if str(input['name']) not in input_variable_names:
                return Response("Unrecognized variable " + input['name'],
                                status=status.HTTP_400_BAD_REQUEST)

        output_variable_names = [var.name for var in system.output_variables.all()]
        outputs = data['data']['outputs']

        if len(output_variable_names) != len(outputs):
            missing_outputs = [var['name'] for var in outputs if var['name'] not in output_variable_names]
            return Response("Incomplete dataset, missing data for output variables " +
                            repr(missing_outputs), status=status.HTTP_400_BAD_REQUEST)

        for output in outputs:
            if output['name'] not in output_variable_names:
                return Response("Unrecognized variable " + output['name'],
                                status=status.HTTP_400_BAD_REQUEST)

        # Get the number of runs
        num_runs = len(inputs[0]['values'])
        for input in inputs:
            if len(input['values']) != num_runs:
                return Response('Invalid number of runs', status=status.HTTP_400_BAD_REQUEST)

        for output in outputs:
            if len(output['values']) != num_runs:
                return Response('Invalid number of runs', status=status.HTTP_400_BAD_REQUEST)

        # Convert the incoming data field to a string
        data['data'] = str(data['data'])
        data['runs'] = num_runs

        serializer = DataSetDetailsSerializer(data=data, context={'system_id': system_id})
        if serializer.is_valid():
            serializer.save()

            # Switch to the data free version of the model for the response
            serializer = DataSetListSerializer(data=serializer.data)
            if serializer.is_valid():

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        system = System.objects.get(pk=system_id)
        serializer = DataSetListSerializer(system.datasets, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def dataset_detail(request, dataset_id, format=None):

    try:
        dataset = DataSet.objects.get(pk=dataset_id)
    except DataSet.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = DataSetDetailsSerializer(dataset)

        # Covert the string representation of the datasets into proper JSON for the response
        serializer_data = serializer.data
        data = serializer_data['data']
        data_json = json.loads(data.replace('\\', '').replace('\'', '\"'))
        serializer_data['data'] = data_json

        return Response(serializer_data)

    elif request.method == 'DELETE':
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def predict(request, system_id, format=None):
    try:
        system = System.objects.get(pk=system_id)
    except System.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Check that the system has a valid surrogate

    # Parse the input data and validate

    # Call the analysis lib

    # Package the response

    # Return

