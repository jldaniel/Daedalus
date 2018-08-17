from rest_framework import serializers
from modeling.models import InputVariable, OutputVariable, System, DataSet, Surrogate


class InputVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputVariable
        fields = ('id', 'name', 'description')


class OutputVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputVariable
        fields = ('id', 'name', 'description')


class DataSetListSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSet
        fields = ('id', 'description', 'created', 'runs', 'system_id')

    def create(self, validated_data):
        validated_data['system_id'] = self.context['system_id']
        dataset = DataSet.objects.create(**validated_data)
        return dataset


class DataSetDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSet
        fields = ('id', 'description', 'created', 'data', 'runs', 'system_id')

    def create(self, validated_data):
        validated_data['system_id'] = self.context['system_id']
        dataset = DataSet.objects.create(**validated_data)
        return dataset


class SurrogateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Surrogate
        fields = ('id', 'created', 'updated')


class SystemSerializer(serializers.ModelSerializer):
    input_variables = InputVariableSerializer(many=True, required=False)
    output_variables = OutputVariableSerializer(many=True, required=False)
    datasets = DataSetListSerializer(many=True, required=False)
    surrogate = SurrogateSerializer(many=False, required=False)

    class Meta:
        model = System
        fields = ('id', 'name', 'description', 'status', 'created', 'updated',
                  'input_variables', 'output_variables', 'datasets', 'surrogate')

    def create(self, validated_data):
        input_variables_data = validated_data.pop('input_variables')
        output_variables_data = validated_data.pop('output_variables')
        system = System.objects.create(**validated_data)

        for input_variable_data in input_variables_data:
            InputVariable.objects.create(system=system, **input_variable_data)

        for output_variable_data in output_variables_data:
            OutputVariable.objects.create(system=system, **output_variable_data)

        return system


