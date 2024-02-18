from django import forms
from .models import Goal, SubGoal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title']

class SubGoalForm(forms.ModelForm):
    class Meta:
        model = SubGoal
        fields = ['is_completed']