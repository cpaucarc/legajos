from django.contrib import admin
from .models import Semestre
# Register your models here.
@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin')