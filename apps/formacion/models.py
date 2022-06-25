import os

from django.core.files.storage import default_storage
from django.db import models

from apps.common.constants import GRADO_CHOICES, FRECUENCIA_CHOICES
from apps.common.models import BaseModel, Institucion, UbigeoPais
from apps.persona.models import Persona


class Universitaria(BaseModel):
    grado_obtenido = models.CharField('Grado Obtenido', max_length=45, choices=GRADO_CHOICES)
    nombre_grado = models.CharField('Nombre Título/Grado', max_length=250)
    centro_estudios = models.ForeignKey(Institucion, on_delete=models.PROTECT)
    facultad = models.CharField('Facultad', max_length=250)
    fecha_inicio = models.DateField('Fecha inicio')
    fecha_fin = models.DateField('Fecha fin', blank=True, null=True)
    pais_estudios = models.ForeignKey(UbigeoPais, on_delete=models.PROTECT, blank=True, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)

    def delete(self, using=None, keep_parents=False):
        for au in self.adjuntouniversitaria_set.all():
            path = default_storage.path(au.ruta)
            if path:
                os.remove(path)
        super(Universitaria, self).delete()


class AdjuntoUniversitaria(BaseModel):
    nombre = models.CharField('Nombre del documento', max_length=200)
    ruta = models.TextField('Ruta del documento', max_length=500)
    universitaria = models.ForeignKey(Universitaria, on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        path = default_storage.path(self.ruta)
        if path:
            os.remove(path)
        super(AdjuntoUniversitaria, self).delete()


class Tecnico(BaseModel):
    centro_estudios = models.ForeignKey(Institucion, on_delete=models.PROTECT)
    nombre_carrera = models.CharField('Nombre de la carrera', max_length=250)
    fecha_inicio = models.DateField('Fecha inicio')
    fecha_fin = models.DateField('Fecha fin')
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)

    def delete(self, using=None, keep_parents=False):
        for at in self.adjuntotecnico_set.all():
            path = default_storage.path(at.ruta)
            if path:
                os.remove(path)
        super(Tecnico, self).delete()


class AdjuntoTecnico(BaseModel):
    nombre = models.CharField('Nombre del documento', max_length=200)
    ruta = models.TextField('Ruta del documento', max_length=500)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        path = default_storage.path(self.ruta)
        if path:
            os.remove(path)
        super(AdjuntoTecnico, self).delete()


class Complementaria(BaseModel):
    capacitacion_complementaria = models.CharField('Capacitación Complementaria', max_length=250)
    centro_estudios = models.ForeignKey(Institucion, on_delete=models.PROTECT)
    pais_estudios = models.ForeignKey(UbigeoPais, on_delete=models.PROTECT, blank=True, null=True)
    frecuencia = models.CharField('Frecuencia', max_length=45, choices=FRECUENCIA_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha_inicio = models.DateField('Fecha inicio', blank=True, null=True)
    fecha_fin = models.DateField('Fecha fin', blank=True, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)

    def delete(self, using=None, keep_parents=False):
        for ac in self.adjuntocomplementaria_set.all():
            path = default_storage.path(ac.ruta)
            if path:
                os.remove(path)
        super(Complementaria, self).delete()


class AdjuntoComplementaria(BaseModel):
    nombre = models.CharField('Nombre del documento', max_length=200)
    ruta = models.TextField('Ruta del documento', max_length=500)
    complementaria = models.ForeignKey(Complementaria, on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        path = default_storage.path(self.ruta)
        if path:
            os.remove(path)
        super(AdjuntoComplementaria, self).delete()
