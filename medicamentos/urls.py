from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Rotas principais
    path('', views.home, name="home-medicamento"),
    path('read/', views.home, name="read-medicamento"),
    
    # Operações de CRUD
    path('add/', views.add, name="add-medicamento"),
    path('detail/<int:id>/', views.detail, name="detail-medicamento"),
    path('edit/<int:id>/', views.edit, name="edit-medicamento"),
    path('remove/<int:id>/', views.remove, name="remove-medicamento"),
    
    # API
    path('api/', views.MedicamentosList.as_view(), name='api-medicamentos'),
    path('api/<int:id>/', views.MedicamentoViewDetail.as_view(), name='api-medicamento-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
