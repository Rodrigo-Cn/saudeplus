from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name="home-medicamento"),
    path('read/', views.home, name="read-medicamento"),
    path('api/', views.MedicamentosList.as_view(), name='api-medicamentos'),
    path('api/<int:id>/', views.MedicamentoViewDetail.as_view(), name='api-medicamento-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
