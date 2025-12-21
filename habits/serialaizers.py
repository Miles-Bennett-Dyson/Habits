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
    def validate(self, attrs):
        if self.instance:
            full_attrs = {
                'related_habit': attrs.get('related_habit', self.instance.related_habit),
                'is_pleasure': attrs.get('is_pleasure', self.instance.is_pleasure),
                'reward': attrs.get('reward', self.instance.reward),
                'periodicity': attrs.get('periodicity', self.instance.periodicity),
            }
        else:
            full_attrs = attrs
        field_validation = HabitFieldsValidator()
        field_validation(full_attrs)
        return attrs

    class Meta:
        model = Habits
        fields = '__all__'
        validators = [DurationValidator(field='duration', )]
