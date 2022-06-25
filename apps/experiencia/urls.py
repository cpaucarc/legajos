from django.urls import path
from apps.experiencia.views import (
    ExperienciaLaboralView, ListaLaboralView, GuardarLaboralView, ConsultaLaboralView,
    SubirArchivosView, ListaArchivosView, EliminarArchivoView,
    DescargarArchivoView, ListaDocenteView, GuardarDocenteView, ConsultaDocenteView,
    ListaAsesorTesisView, GuardarAsesorTesisView, ConsultaAsesorTesisView, ConsultaEvaluadorProyectoView,
    ListaEvaluadorProyectoView, GuardarEvaluadorProyectoView
)
app_name = 'experiencia'
urlpatterns = [
    path('experiencia-laboral/<str:pk>', ExperienciaLaboralView.as_view(), name='experiencia_laboral'),
    path('consulta-laboral/<str:pk>', ConsultaLaboralView.as_view(), name='consulta_laboral'),
    path('consulta-docente/<str:pk>', ConsultaDocenteView.as_view(), name='consulta_docente'),
    path('consulta-asesor-tesis/<str:pk>', ConsultaAsesorTesisView.as_view(), name='consulta_asesor_tesis'),
    path('consulta-evaluador-proyecto/<str:pk>', ConsultaEvaluadorProyectoView.as_view(),
         name='consulta_evaluador_proyecto'),
    path('lista-laboral/<str:pk>', ListaLaboralView.as_view(), name='lista_laboral'),
    path('lista-docente/<str:pk>', ListaDocenteView.as_view(), name='lista_docente'),
    path('lista-asesor-tesis/<str:pk>', ListaAsesorTesisView.as_view(), name='lista_asesor_tesis'),
    path('lista-evaluador-proyecto/<str:pk>', ListaEvaluadorProyectoView.as_view(), name='lista_evaluador_proyecto'),
    path('guardar-laboral/<str:pk>/', GuardarLaboralView.as_view(), name='guardar_laboral'),
    path('guardar-docente/<str:pk>/', GuardarDocenteView.as_view(), name='guardar_docente'),
    path('guardar-asesor-tesis/<str:pk>/', GuardarAsesorTesisView.as_view(), name='guardar_asesor_tesis'),
    path('guardar-evaluador-proyecto/<str:pk>/', GuardarEvaluadorProyectoView.as_view(),
         name='guardar_evaluador_proyecto'),
    path('lista-archivos/<str:pk>/<str:tipo>/', ListaArchivosView.as_view(), name='listar_archivos'),
    path('subir-archivos/<str:pk>/<str:tipo>/', SubirArchivosView.as_view(), name='subir_archivos'),
    path('eliminar-archivo/<str:pk>/<str:tipo>/', EliminarArchivoView.as_view(), name='eliminar_archivo'),
    path('descargar-archivo/<str:pk>/<str:tipo>/', DescargarArchivoView.as_view(), name='descargar_archivo'),
]
