from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Rotas tradicionais (HTML)
    path('', views.home, name='home'),
    path('read/', views.home, name='read-medico'),
    path('detail/<int:medico_id>/', views.detail, name='detail-medico'),
    path('detail2/<int:medico_id>/', views.detail2, name='detail2-medico'),
    path('edit/<int:medico_id>/', views.edit, name='edit-medico'),
    path('perfil/', views.perfil, name='perfil-medico'),
    path('editperfil/', views.editperfil, name='edit-perfil'),
    path('remove/<int:medico_id>/', views.remove, name='remove-medico'),
    path('add/', views.add, name='add-medico'),
    # Endpoints da API
    path('api/', views.MedicosList.as_view(), name='api-medicos'),
    path('api/<int:id>/', views.MedicoViewDetail.as_view(), name='api-medico-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
