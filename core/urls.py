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
<<<<<<< HEAD
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
=======
    # re_path(r'^belt/$', views.belt)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


>>>>>>> b3c4c0737ba351f30adbe43645691b5f7f16cfb4





