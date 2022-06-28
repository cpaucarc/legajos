from django.contrib import admin

from apps.common.models import Institucion, CatalogoIdiomas, Colegio


@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('ruc', 'name')


@admin.register(CatalogoIdiomas)
class CatalogoIdiomasAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')

@admin.register(Colegio)
class ColegiosAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'name')