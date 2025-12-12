from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from habits.models import Habits


class HabitSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        related_habit = validated_data.get('related_habit')
        reward = validated_data.get('reward')
        if not related_habit and not reward:
            raise ValidationError('Необходимо указать вознаграждение ИЛИ связанную привычку')
        if related_habit and reward:
            raise ValidationError('Можно указать только вознаграждение ИЛИ связанную привычку')

        habit = Habits.objects.create(**validated_data)
        return habit

    class Meta:
        model = Habits
        fields = '__all__'
