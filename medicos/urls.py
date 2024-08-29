from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('<int:medico_id>/', views.home, name='home-medico'),
]
