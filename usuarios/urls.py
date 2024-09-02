from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('adm/', views.home, name='home-adm'),
    path('login/', views.custom_login_view, name='login'), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)