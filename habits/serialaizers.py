from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from habits.models import Habits
from habits.services import setting_next_date
from habits.validators import DurationValidator, HabitFieldsValidator


class HabitSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        periodicity = validated_data.get('periodicity')
        validated_data['next_due_date'] = setting_next_date(periodicity)
        habit = Habits.objects.create(**validated_data)
        return habit

    class Meta:
        model = Habits
        fields = '__all__'
        validators = [DurationValidator(field='duration', ), HabitFieldsValidator()]
