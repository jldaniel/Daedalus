from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from modeling.models import System, DataSet, SurrogateModel
from modeling.serializers import SystemSerializer, DataSetListSerializer, DataSetDetailsSerializer

from kaolin import Surrogate

import json
import numpy as np


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
    if system.surrogate_id is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Parse the input data and validate
        # Validate the incoming data field
    data = request.data

    input_variable_names = [var.name for var in system.input_variables.all()]
    inputs = data['inputs']

    if len(input_variable_names) != len(inputs):
        missing_inputs = [var['name'] for var in inputs if var['name'] not in input_variable_names]
        return Response("Incomplete dataset, missing data for input variables " +
                        repr(missing_inputs), status=status.HTTP_400_BAD_REQUEST)

    for input in inputs:
        if str(input['name']) not in input_variable_names:
            return Response("Unrecognized variable " + input['name'],
                            status=status.HTTP_400_BAD_REQUEST)

    # Get the number of runs
    num_runs = len(inputs[0]['values'])
    for input in inputs:
        if len(input['values']) != num_runs:
            return Response('Invalid number of runs', status=status.HTTP_400_BAD_REQUEST)

    # Gather the values for the points to predict at
    prediction_points = []
    for i in range(num_runs):
        point = []
        for input in inputs:
            point.append(input['values'][i])

        prediction_points.append(point)

    # Load the surrogate
    try:
        surrogate = Surrogate().load(system.surrogate.location)
    except Exception as ex:
        return Response(ex, status=status.HTTP_400_BAD_REQUEST)

    # Predict the points
    y = surrogate.predict(prediction_points)

    # Package the response
    response_data = {}
    response_data['inputs'] = inputs
    response_data['outputs'] = []

    outputs_variable_names = [var.name for var in system.output_variables.all()]

    for idx, output_name in enumerate(outputs_variable_names):
        output_data = {}
        output_data['name'] = output_name
        output_data['values'] = [point[i] for point in y]
        response_data['outputs'].append(output_data)

    # Return
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def adapt(request, system_id, format=None):
    # POST Model
    #{'sites': float,
    # 'inputs': [
    #       {'name': string,
    #        'lower_bound': float,
    #        'upper_bound': float}
    #    ]
    # }

    # Load the system
    try:
        system = System.objects.get(pk=system_id)
    except System.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Check if the surrogate isnt ready read
    if system.status == 'ERROR':
        return Response("System is in an ERROR state", status=status.HTTP_400_BAD_REQUEST)

    if system.status == 'BUSY':
        return Response("System is currently busy", status=status.HTTP_400_BAD_REQUEST)

    n_sites = request.data['n_designs']
    bounds_json = request.data['inputs']

    bounds_dict = {}
    for bound in bounds_json:
        bounds_dict[bound['name']] = [bound['lower_bound'], bound['upper_bound']]

    # Check that all inputs are accounted for
    input_variable_names = [var.name for var in system.input_variables.all()]
    bounds = []
    for name in input_variable_names:
        if name not in bounds_dict.keys():
            return Response("Bounds not set for model input variable " + name, status=status.HTTP_400_BAD_REQUEST)

        bounds.append(bounds_dict[name])

    bounds = np.array(bounds)
    print("BOUNDS")
    print(repr(bounds))
    # RESPONSE MODEL
    # [{'name': string, 'value': float}]

    designs_response = []
    designs = None
    if system.status == 'CREATED':
        # Model is not trained, generate initial DOE
        designs = Surrogate().adapt(bounds, n_sites)

    if system.status == 'READY':
        # Load the surrogate
        surrogate = SurrogateModel.objects.get(system_id=system.id)
        surrogate_location = surrogate.location
        surrogate = Surrogate().load(surrogate_location)
        designs = surrogate.adapt(bounds, n_sites)

    print("DESIGNS")
    print(repr(designs))
    for idx, design in enumerate(designs):
        design_json = []
        for idv, name in enumerate(input_variable_names):
            design_dict = dict()
            design_dict['name'] = name
            design_dict['value'] = design[idv]
            design_json.append(design_dict)

        designs_response.append(design_json)

    return Response(designs_response, status=status.HTTP_201_CREATED)




