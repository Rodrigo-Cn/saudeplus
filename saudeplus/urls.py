from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='registration/login.html'), name="login"),
    path('medico/', include('medicos.urls')),

]
