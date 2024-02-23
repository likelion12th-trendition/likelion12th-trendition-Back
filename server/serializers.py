from rest_framework import serializers
from .models import Goal, SubGoal

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'title']

class SubGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubGoal
        fields = ['id', 'title', 'is_completed']
