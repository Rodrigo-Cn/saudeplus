from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home,  name='home'),
    path('read/', views.read, name='read-medico'),
    path('detail/<int:medico_id>/', views.detail, name='detail-medico'),
    path('detail2/<int:medico_id>/', views.detail2, name='detail2-medico'),
    path('edit/<int:medico_id>/', views.edit, name='edit-medico'),
    path('perfil/', views.perfil, name='perfil-medico'),
    path('editperfil/', views.editperfil, name='edit-perfil'),
    path('remove/<int:medico_id>/', views.remove, name='remove-medico'),
    path('add/', views.add, name='add-medico')
]
