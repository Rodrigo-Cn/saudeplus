from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('read/', views.read, name='read-paciente'),
    path('add/', views.add, name='add-paciente')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
