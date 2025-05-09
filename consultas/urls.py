from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('read/', views.read, name='read-consulta'),
    path('detail/<int:consulta_id>/', views.detail, name='detail-consulta'),
    path('edit/<int:consulta_id>/', views.edit, name='edit-consulta'),
    path('remove/<int:consulta_id>/', views.remove, name='remove-consulta'),
    path('add/', views.add, name='add-consulta'),
    path('detail/', views.detail, name='detail-consulta'),
    path('editReceita/<int:receita_id>/', views.editar_receita, name='edit-consulta-receita'),
    path('api/', views.ConsultaList.as_view()),
    path('api/<int:id>/', views.ConsultaViewDetail.as_view()),
]
