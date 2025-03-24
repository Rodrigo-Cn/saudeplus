from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("select2/", include("django_select2.urls")),
    path('', include('medicos.urls')),
    path('medico/', include('medicos.urls')),
    path('admin/', admin.site.urls),
    path('usuario/', include('usuarios.urls')),
    path('conta/', include('usuarios.urls')),
    path('conta/', include('django.contrib.auth.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('medicamento/', include('medicamentos.urls')),
    path('consulta/', include('consultas.urls')),
    path('cid/', include('cids.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
