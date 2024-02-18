from django.contrib import admin
from django.urls import path
from join.views import signup, login
from server.views import home, goal, subgoal

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", home, name="home"),
    path("join/", signup, name='signup'),
    path("login/", login, name='login'),
    path('goal/', goal, name="goal"),
    path('subgoal/', subgoal, name="subgoal"),
]
