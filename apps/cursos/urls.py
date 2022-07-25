from django.urls import path
from .views import (CursosCreateView, CursosGuardarView, ListaCursosView,
                    RsuCreateView, RsuGuardarView, ListaRsuView)

app_name = 'cursos'

urlpatterns = [
    path('agregar-cursos/<str:pk>', CursosCreateView.as_view(), name='agregar_cursos'),
    path('guardar-cursos/<str:pk>/<str:inst_id>/<str:sem_id>/<str:esc>/<str:cursos>', CursosGuardarView.as_view(), name='guardar_cursos'),
    path('lista-cursos/<str:pk>/', ListaCursosView.as_view(), name='lista_cursos'),

    path('agregar-rsu/<str:pk>', RsuCreateView.as_view(), name='agregar_rsu'),
    path('guardar-rsu/<str:pk>/<str:titulo>/<str:lugar>/<str:descripcion>/<str:inicio>/<str:fin>/<slug:en_empresa>/<str:ruc>/<str:empresa>', RsuGuardarView.as_view(), name='guardar_rsu'),
    path('lista-rsu/<str:pk>', ListaRsuView.as_view(), name='lista_rsu'),
]
