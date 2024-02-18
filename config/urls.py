from django.contrib import admin
from django.urls import path, include
from join.views import *
from server.views import home, goal, subgoal
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", home, name="home"),
    #path("join/", signup, name='signup'),
    #path("login/", login, name='login'),
    path('goal/', goal, name="goal"),
    path('subgoal/', subgoal, name="subgoal"),
    path('join/', include('join.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)