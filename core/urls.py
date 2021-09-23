from os import name
from django import urls
from django.contrib import admin
from django.urls import path, re_path
from . import views

from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('production/count', views.production_count, name="production_count"),
    path('machines/data', views.machine_data, name="machine_data"),
    path('belts/avg', views.belts_avg, name="belts_avg"),
    # re_path(r'^belt/$', views.belt)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)







