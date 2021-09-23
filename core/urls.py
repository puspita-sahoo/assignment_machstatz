from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ping, name="ping"),
    path('production/count', views.production_count, name="production_count"),
    path('machines/data', views.machine_data, name="machine_data"),
    path('belts/avg', views.belts_avg, name="belts_avg"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

