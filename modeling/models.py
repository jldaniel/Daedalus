
from django.db import models

SYSTEM_STATUS = (
    ('CREATED', 'CREATED'),
    ('READY', 'READY'),
    ('TRAINING', 'TRAINING'),
    ('ERROR', 'ERROR'),
)


class System(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=120, blank=True, default='')
    description = models.TextField(null=True)
    status = models.CharField(max_length=8, choices=SYSTEM_STATUS, default=SYSTEM_STATUS[0][0])


class InputVariable(models.Model):
    name = models.CharField(max_length=120, blank=False)
    description = models.TextField()
    system = models.ForeignKey(System, related_name='input_variables', on_delete=models.CASCADE)


class OutputVariable(models.Model):
    name = models.CharField(max_length=120, blank=False)
    description = models.TextField()
    system = models.ForeignKey(System, related_name='output_variables', on_delete=models.CASCADE)


class DataSet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    system = models.ForeignKey(System, related_name='datasets', on_delete=models.CASCADE, null=True)
    runs = models.IntegerField(default=0)
    data = models.TextField(null=True)  # JSON Representation of the data


class Surrogate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    system = models.ForeignKey(System, related_name='surrogate', on_delete=models.SET_NULL, null=True)
    score = models.FloatField(null=True)
    location = models.TextField(null=True)
    # TODO Add surrogate metdata



