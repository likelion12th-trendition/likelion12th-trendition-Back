from django.contrib import admin
from django.urls import path
from join.views import signup, login

urlpatterns = [
    path("admin/", admin.site.urls),
    path("join/", signup, name='signup'),
    path("login/", login, name='login'),
]
