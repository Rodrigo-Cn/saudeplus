from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,  name='home-cid'),
    path('api/', views.CidList.as_view()),
    path('api/<int:id>/', views.CidViewDetail.as_view()),
]
