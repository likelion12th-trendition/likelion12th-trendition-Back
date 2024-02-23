from django.contrib import admin
from django.urls import path, include
from join.views import *
from django.conf import settings
from .views import home, create_goal, update_goal, delete_goal, create_subgoal, update_subgoal, delete_subgoal
from .views import completed_subgoals, subgoals_by_goal, goals_by_username

urlpatterns = [
    path('', home),
    path("goal/create/", create_goal),
    path("goal/update/<int:goal_id>", update_goal),
    path('goal/delete/<int:goal_id>', delete_goal),
    path("subgoal/create/<int:goal_id>", create_subgoal),
    path("subgoal/update/<int:subgoal_id>", update_subgoal),
    path('subgoal/delete/<int:subgoal_id>', delete_subgoal),
    path('subgoal/completed/', completed_subgoals),
    path('subgoal/bygaol/<int:goal_id>', subgoals_by_goal),
    path('goal/<str:username>/', goals_by_username),
]