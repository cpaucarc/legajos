from django.urls import path
from .views import (CursosCreateView, CursosGuardarView, ListaCursosView)

app_name = 'cursos'

urlpatterns = [
    # path('agregar-cursos/<str:pk>', cursos_create_view, name='agregar-cursos'),
    path('agregar-cursos/<str:pk>', CursosCreateView.as_view(), name='agregar_cursos'),
    path('guardar-cursos/<str:pk>/<str:inst_id>/<str:sem_id>/<str:esc>/<str:cursos>', CursosGuardarView.as_view(), name='guardar_cursos'),
    path('lista-cursos/<str:pk>/', ListaCursosView.as_view(), name='lista_cursos'),
]
