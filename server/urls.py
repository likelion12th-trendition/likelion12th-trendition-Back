from django.contrib import admin
from django.urls import path, include
from join.views import *
from django.conf import settings
from .views import home, create_goal, update_goal, delete_goal, create_subgoal, update_subgoal, delete_subgoal, create_goal_all

urlpatterns = [
    path('', home),
    path("goal/create/", create_goal),
    path("goal/createall/", create_goal_all),
    path("goal/update/<int:goal_id>", update_goal),
    path('goal/delete/<int:goal_id>', delete_goal),
    path("subgoal/create/<int:goal_id>", create_subgoal),
    path("subgoal/update/<int:subgoal_id>", update_subgoal),
    path('subgoal/delete/<int:subgoal_id>', delete_subgoal),
]