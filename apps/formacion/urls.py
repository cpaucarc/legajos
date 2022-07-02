from django.urls import path
from apps.formacion.views import (GuardarUniversitariaView, ListaUniversitariaView, SubirArchivosView,
                                  ListaArchivosView, EliminarArchivoView, ConsultaUniversitariaView,
                                  DescargarArchivoView, ConsultaTecnicoView, ListaTecnicoView, GuardarTecnicoView,
                                  ConsultaComplementariaView, ListaComplementariaView, GuardarComplementariaView,
                                  EliminarComplementariaView, EliminarTecnicoView, EliminarUniversitariaView)
from apps.formacion.views import (
    FormacionAcademicaView
)

app_name = 'formacion'
urlpatterns = [
    path('formacion-academica/<str:pk>', FormacionAcademicaView.as_view(), name='formacion_academica'),
    path('consulta-universitaria/<str:pk>', ConsultaUniversitariaView.as_view(), name='consulta_universitaria'),
    path('consulta-tecnico/<str:pk>', ConsultaTecnicoView.as_view(), name='consulta_tecnico'),
    path('consulta-complementaria/<str:pk>', ConsultaComplementariaView.as_view(), name='consulta_complementaria'),
    path('lista-Universitaria/<str:pk>', ListaUniversitariaView.as_view(), name='lista_universitaria'),
    path('lista-tecnico/<str:pk>', ListaTecnicoView.as_view(), name='lista_tecnico'),
    path('lista-complementaria/<str:pk>', ListaComplementariaView.as_view(), name='lista_complementaria'),
    path('guardar-universitaria/<str:pk>/', GuardarUniversitariaView.as_view(), name='guardar_universitaria'),
    path('guardar-tecnico/<str:pk>/', GuardarTecnicoView.as_view(), name='guardar_tecnico'),
    path('guardar-complementaria/<str:pk>/', GuardarComplementariaView.as_view(), name='guardar_complementaria'),
    path('lista-archivos/<str:pk>/<str:tipo>/', ListaArchivosView.as_view(), name='listar_archivos'),
    path('subir-archivos/<str:pk>/<str:tipo>/', SubirArchivosView.as_view(), name='subir_archivos'),
    path('eliminar-archivo/<str:pk>/<str:tipo>/', EliminarArchivoView.as_view(), name='eliminar_archivo'),
    path('descargar-archivo/<str:pk>/<str:tipo>/', DescargarArchivoView.as_view(), name='descargar_archivo'),
    path('eliminar-complementaria/<str:pk>', EliminarComplementariaView.as_view(), name='eliminar_complementaria'),
    path('eliminar-tecnico/<str:pk>', EliminarTecnicoView.as_view(), name='eliminar_tecnico'),
    path('eliminar-universitaria/<str:pk>', EliminarUniversitariaView.as_view(), name='eliminar_universitaria'),
]
