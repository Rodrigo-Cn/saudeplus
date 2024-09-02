from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('read/', views.read, name='read-consulta'),
    path('detail/<int:consulta_id>/', views.detail, name='detail-consulta'),
    path('edit/<int:consulta_id>/', views.edit, name='edit-consulta'),
    path('remove/<int:consulta_id>/', views.remove, name='remove-consulta'),
    path('add/', views.add, name='add-consulta')
]
