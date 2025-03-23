from django.urls import include, path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name="home-medicamento"),
    path('add/', views.add, name="add-medicamento"),
    path('detail/<int:id>/', views.detail, name="detail-medicamento"),
    path('edit/<int:id>/', views.edit, name="edit-medicamento"), 
    path('remove/<int:id>/', views.remove, name="remove-medicamento"), 
    path('api/', views.MedicamentosList.as_view()),
    path('api/<int:id>/', views.MedicamentoViewDetail.as_view()),
]
