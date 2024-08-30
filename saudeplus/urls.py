from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('medicos.urls')),
    path('admin/', admin.site.urls),
    path('usuario/', include('usuarios.urls')),
    path('conta/', include('django.contrib.auth.urls')),
]
