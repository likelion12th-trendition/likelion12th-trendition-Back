from django import forms
from .models import Goal, SubGoal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        field = ['title']

class SubGoalForm(forms.ModelForm):
    class Meta:
        model = SubGoal
        field = ['title', 'is_completed']