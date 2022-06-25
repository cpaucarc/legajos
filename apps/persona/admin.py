from django.contrib import admin

from apps.persona.models import Facultad, Departamento


@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'facultad')
