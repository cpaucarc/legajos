from django.db import models

from apps.common.models import Institucion
from apps.persona.models import Persona


# Create your models here.
class Semestre(models.Model):
    nombre = models.CharField(max_length=7)
    fecha_inicio = models.DateField('Fecha inicio')
    fecha_fin = models.DateField('Fecha fin')

    def __str__(self):
        return '{nombre}'.format(nombre=self.nombre)


class CursoDictado(models.Model):
    escuela = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, blank=False, null=False)
    semestre = models.ForeignKey(Semestre, on_delete=models.PROTECT, blank=False, null=False)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        return '{semestre} - {curso}'.format(semestre=self.semestre, curso=self.curso)
