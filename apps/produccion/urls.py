from django.urls import path
from apps.produccion.views import (ListaCientificaView, GuardarCientificaView, SubirArchivosView,
                                   ListaArchivosView, EliminarArchivoView, DescargarArchivoView, ConsultaCientificaView,
                                   EliminarCientificaView, CientificaView)

app_name = 'produccion'
urlpatterns = [
    path('cientifica/<str:pk>', CientificaView.as_view(), name='cientifica'),
    path('lista-cientifica/<str:pk>', ListaCientificaView.as_view(), name='lista_cientifica'),
    path('consulta-cientifica/<str:pk>', ConsultaCientificaView.as_view(), name='consulta_cientifica'),
    path('guardar-cientifica/<str:pk>/', GuardarCientificaView.as_view(), name='guardar_cientifica'),
    path('lista-archivos/<str:pk>/', ListaArchivosView.as_view(), name='listar_archivos'),
    path('subir-archivos/<str:pk>/', SubirArchivosView.as_view(), name='subir_archivos'),
    path('eliminar-cientifica/<str:pk>/', EliminarCientificaView.as_view(), name='eliminar_cientifica'),
    path('eliminar-archivo/<str:pk>/', EliminarArchivoView.as_view(), name='eliminar_archivo'),
    path('descargar-archivo/<str:pk>/', DescargarArchivoView.as_view(), name='descargar_archivo'),
    path('eliminar-cientifica/<str:pk>', EliminarCientificaView.as_view(), name='eliminar_cientifica'),
]
