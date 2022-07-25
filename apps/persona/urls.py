from django.urls import path
from apps.persona.views import (BuscarPersonaAPIView, PersonaCreateView, ListaPersonaView, PersonaUpdateView,
                                EliminarPersonaView, ProvinciaView, DistritoView, DepartamentosPorFacultadView,
                                ExportarCVView, DescargarCVPdf, DescargarCVPdfDet,
                                ColegiaturaGuardarView, ListaColegiaturaView)

app_name = 'persona'
urlpatterns = [
    path('crear-persona', PersonaCreateView.as_view(), name='crear_persona'),
    path('buscar-persona', BuscarPersonaAPIView.as_view(), name='buscar-persona'),
    path('listar-persona', ListaPersonaView.as_view(), name='listar_persona'),
    path('editar-persona/<str:pk>/', PersonaUpdateView.as_view(), name='editar_persona'),
    path('exportar-cv/<str:pk>/', ExportarCVView.as_view(), name='exportar_cv'),
    path('descargar-cv/<str:pk>/', DescargarCVPdf.as_view(), name='descargar_pdf'),
    path('descargar-cv-det/<str:pk>/', DescargarCVPdfDet.as_view(), name='descargar_pdf_det'),
    path('eliminar/<str:pk>', EliminarPersonaView.as_view(), name='eliminar_persona'),
    path('consulta-departamento/', DepartamentosPorFacultadView.as_view(), name='consulta_departamento'),
    path('provincias/', ProvinciaView.as_view(), name='provincias'),
    path('distritos/', DistritoView.as_view(), name='distritos'),

    path('guardar-colegiatura/<str:pk>/<str:colegios>/<str:sedes>/<str:codigos>/<str:estados>', ColegiaturaGuardarView.as_view(), name='guardar_colegiatura'),
    path('lista-colegiatura/<str:pk>', ListaColegiaturaView.as_view(), name='lista_colegiatura'),
]
