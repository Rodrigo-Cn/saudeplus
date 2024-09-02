from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('<int:medico_id>/', views.home,  name='home-medico'), #URL TEMPORÁRIA APENAS PARA TESTES
    path('read/', views.read, name='read-medico'),
    path('detail/<int:medico_id>/', views.detail, name='detail-medico'),
    path('edit/<int:medico_id>/', views.edit, name='edit-medico'),
    path('remove/<int:medico_id>/', views.remove, name='remove-medico')
]
