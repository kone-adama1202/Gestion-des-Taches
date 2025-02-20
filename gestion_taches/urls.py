# gestion_taches/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('taches.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]