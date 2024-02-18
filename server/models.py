from django.db import models
from join.models import CustomUser

# Create your models here.
class Goal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100) # 목표 최대 글자 수 100

class SubGoal(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_completed = models.BooleanField(default = False)
