
from kaolin import Surrogate
from modeling.models import SurrogateModel

import numpy as np

from django.conf import settings
import json
import os


# TODO: Handle errors
def train_initial_surrogate(system, dataset):

    # Get the json representation of the dataset data
    dataset_data_json = dataset.data
    dataset_data = json.loads(dataset_data_json.replace('\\', '').replace('\'', '\"'))

    input_variable_names = [var.name for var in system.input_variables.all()]
    input_vars = dataset_data['inputs']

    output_variable_names = [var.name for var in system.output_variables.all()]
    output_vars = dataset_data['outputs']

    # Build the training data input arrays
    n_runs = dataset.runs
    ndim_in = len(input_variable_names)
    ndim_out = len(output_variable_names)

    x_train = np.empty((n_runs, ndim_in))
    y_train = np.empty((n_runs, ndim_out))
    for i in range(n_runs):

        for j, var in enumerate(input_vars):
            x_train[i, j] = var['values'][i]

        for j, var in enumerate(output_vars):
            y_train[i, j] = var['values'][i]

    print('x_train', repr(x_train))
    print('y_train', repr(y_train))
    # Train the surrogate model
    surrogate = Surrogate()
    surrogate.fit(x_train, y_train)

    surrogate_dir = system.name.replace(' ', '_') + '_' + str(system.id) + '.surrogate'
    save_dir = os.path.join(settings.SURROGATES_ROOT, surrogate_dir)

    if not os.path.exists(settings.SURROGATES_ROOT):
        os.makedirs(settings.SURROGATES_ROOT)

    surrogate.save(save_dir)

    surrogate_model = SurrogateModel.objects.create(
        system_id=system.id,
        score=surrogate.cv_metrics['r2_score'],
        location=save_dir,
    )

    surrogate_model.datasets.set([dataset])

    dataset.applied = True
    system.surrogate.set([surrogate_model])
    system.status = 'READY'

    dataset.save()
    system.save()














