from django.urls import path
from .views import CustomLoginView
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('adm/', views.home, name='home-adm'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)