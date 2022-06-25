from django.urls import path
from apps.distincion.views import (ListaDistincionView, GuardarDistincionView, SubirArchivosView,
                                   ListaArchivosView, EliminarArchivoView, DescargarArchivoView, ConsultaDistincionView,
                                   EliminarDistincionView, DistincionView)

app_name = 'distincion'
urlpatterns = [
    path('distincion-premio/<str:pk>', DistincionView.as_view(), name='distincion'),
    path('lista-distincion/<str:pk>', ListaDistincionView.as_view(), name='lista_distincion'),
    path('consulta-distincion/<str:pk>', ConsultaDistincionView.as_view(), name='consulta_distincion'),
    path('guardar-distincion/<str:pk>/', GuardarDistincionView.as_view(), name='guardar_distincion'),
    path('lista-archivos/<str:pk>/', ListaArchivosView.as_view(), name='listar_archivos'),
    path('subir-archivos/<str:pk>/', SubirArchivosView.as_view(), name='subir_archivos'),
    path('eliminar-distincion/<str:pk>/', EliminarDistincionView.as_view(), name='eliminar_distincion'),
    path('eliminar-archivo/<str:pk>/', EliminarArchivoView.as_view(), name='eliminar_archivo'),
    path('descargar-archivo/<str:pk>/', DescargarArchivoView.as_view(), name='descargar_archivo'),
    path('eliminar-distincion/<str:pk>', EliminarDistincionView.as_view(), name='eliminar_distincion'),
]
