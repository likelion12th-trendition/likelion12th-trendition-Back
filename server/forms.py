from django import forms
from .models import Goal, SubGoal
from django.forms import formset_factory

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title']

GoalFormSet = formset_factory(GoalForm, max_num=6)

class SubGoalForm(forms.ModelForm):
    class Meta:
        model = SubGoal
        fields = ['is_completed']