from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import PacientesList, PacienteDetail

urlpatterns = [
    path('read/', views.read, name='read-paciente'),
    path('adm/', views.adm, name='adm-paciente'),
    path('add/', views.add, name='add-paciente'),
    path('remove/<int:paciente_id>', views.remove, name='remove-paciente'),
    path('edit/<int:paciente_id>', views.edit, name="edit-paciente"),
    path('registro/<int:paciente_id>', views.registro, name="read-registro"),
    path('api/', PacientesList.as_view()),
    path(r'api/<int:pk>/', PacienteDetail.as_view()),
]
