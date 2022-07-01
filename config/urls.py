from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.login.urls', namespace='login')),
    path('', include('apps.persona.urls', namespace='persona')),
    path('experiencia/', include('apps.experiencia.urls', namespace='experiencia')),
    path('formacion/', include('apps.formacion.urls', namespace='formacion')),
    path('idioma/', include('apps.idioma.urls', namespace='idioma')),
    path('produccion/', include('apps.produccion.urls', namespace='produccion')),
    path('distincion/', include('apps.distincion.urls', namespace='distincion')),
    path('cursos/', include('apps.cursos.urls', namespace='cursos')),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
