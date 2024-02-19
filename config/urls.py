from django.contrib import admin
from django.urls import path, include, re_path
from join.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", include('server.urls')),
    path('join/', include('join.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)