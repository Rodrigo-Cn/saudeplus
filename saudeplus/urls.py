from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('medicos.urls')),
    path('medico/', include('medicos.urls')),
    path('admin/', admin.site.urls),
    path('usuario/', include('usuarios.urls')),
    path('conta/', include('django.contrib.auth.urls')),
    path('paciente/', include('pacientes.urls')),
    path('medicamento/', include('medicamentos.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
