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

    class Meta:
        ordering = ['semestre', 'institucion', 'escuela', 'curso']

class ResponsabilidadSocial(models.Model):
    titulo = models.CharField('Título', max_length=400)
    descripcion = models.TextField('Descripción', blank=True, null=True)
    fecha_inicio = models.DateField('Fecha de inicio')
    fecha_fin = models.DateField('Fecha de fin')
    lugar = models.CharField('Lugar', max_length=400)
    empresa = models.CharField('Empresa', max_length=400, blank=True, null=True)
    ruc = models.CharField('RUC', max_length=11, blank=True, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return '{} por {}'.format(self.titulo, self.persona)

    class Meta:
        ordering = ['-fecha_fin', 'titulo']
