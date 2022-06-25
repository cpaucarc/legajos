from django.urls import path
from apps.idioma.views import IdiomaCreateView, ListaIdiomasView, IdiomaUpdateView, EliminarIdiomaView

app_name = 'idioma'
urlpatterns = [
    path('crear/<str:pk>', IdiomaCreateView.as_view(), name='crear_idioma'),
    path('editar/<str:pk>', IdiomaUpdateView.as_view(), name='editar_idioma'),
    path('listar-idiomas/<str:persona_id>', ListaIdiomasView.as_view(), name='listar_idiomas'),
    path('eliminar-idioma/<str:pk>', EliminarIdiomaView.as_view(), name='eliminar_idioma'),
]
