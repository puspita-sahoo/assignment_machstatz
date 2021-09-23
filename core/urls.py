from os import name
from django import urls
from django.contrib import admin
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('production/count', views.production_count, name="production_count"),
    path('machines/data', views.machine_data, name="machine_data"),
    path('belts/avg', views.belts_avg, name="belts_avg"),
    # re_path(r'^belt/$', views.belt)
]

"""
(r'^get_item/$', get_item)
And in your view:

def get_item(request):
    id = int(request.GET.get('id'))
    type = request.GET.get('type', 'default')
    
"""





