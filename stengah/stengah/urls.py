from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from . import settings
from api.endpoints import api

urlpatterns = [
    path('', include('web.urls')),
    path('api/', api.urls),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
