from django.urls import path
from .views import (cursos_create_view)

app_name = 'cursos'

urlpatterns = [
    path('agregar-cursos/<str:pk>', cursos_create_view, name='agregar-cursos'),
]
