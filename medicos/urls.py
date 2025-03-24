from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('read/', views.home, name='read-medico'),
    path('api/', views.MedicosList.as_view(), name='api-medicos'),
    path('api/<int:id>/', views.MedicoViewDetail.as_view(), name='api-medico-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
