import os

from django.core.files.storage import default_storage

from apps.common.models import BaseModel, Institucion, UbigeoPais
from django.db import models

from apps.persona.models import Persona


class Distincion(BaseModel):
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT)
    distincion = models.CharField('Distinción', max_length=250)
    descripcion = models.TextField('Descripción', max_length=600)
    pais = models.ForeignKey(UbigeoPais, on_delete=models.PROTECT)
    web_referencia = models.CharField('Web referencia', max_length=250)
    fecha = models.DateField()
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)

    def delete(self, using=None, keep_parents=False):
        for au in self.adjuntodistincion_set.all():
            path = default_storage.path(au.ruta)
            if path:
                os.remove(path)
        super(Distincion, self).delete()


class AdjuntoDistincion(BaseModel):
    nombre = models.CharField('Nombre del documento', max_length=200)
    ruta = models.TextField('Ruta del documento', max_length=500)
    distincion = models.ForeignKey(Distincion, on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        path = default_storage.path(self.ruta)
        if path:
            os.remove(path)
        super(AdjuntoDistincion, self).delete()
