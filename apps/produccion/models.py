import os

from django.core.files.storage import default_storage
from django.db import models

from apps.common.constants import CATEGORIA_TRABAJO_CHOICES, TIPO_OBRA_CHOICES, FUNCION_CHOICES, TIPO_CITA_CHOICES, \
    ORDEN_AUTORIA_CHOICES, TIPO_DOC_ADJUNTO_CHOICES, TIPO_CONGRESO_CHOICES
from apps.common.models import BaseModel, UbigeoPais
from apps.persona.models import Persona


class Cientifica(BaseModel):
    categoria_trabajo = models.CharField('Categoria de trabajo', max_length=45, choices=CATEGORIA_TRABAJO_CHOICES)
    tipo_obra = models.CharField('Tipo de obra', max_length=45, choices=TIPO_OBRA_CHOICES)
    funcion = models.CharField('Función', max_length=45, choices=FUNCION_CHOICES)
    titulo = models.CharField('Título', max_length=250)
    sub_titulo = models.CharField('Sub-Título', max_length=250)
    revista = models.CharField('Revista', max_length=250)
    volumen = models.PositiveIntegerField(blank=True, null=True)
    fasciculo = models.PositiveIntegerField(blank=True, null=True)
    rango_paginas = models.CharField('Rango de páginas', max_length=45)
    fecha_publicacion = models.DateField()
    tipo_cita = models.CharField('Tipo de cita', max_length=45, choices=TIPO_CITA_CHOICES, blank=True, null=True)
    cita = models.CharField('Cita', max_length=250, blank=True, null=True)
    descripcion = models.CharField('Descripción', max_length=250)
    orden_autoria = models.CharField('Orden autoría', max_length=10, choices=ORDEN_AUTORIA_CHOICES)
    autor = models.CharField('Autor', max_length=100)
    tipo_congreso = models.CharField('Tipo de congreso', max_length=45, choices=TIPO_CONGRESO_CHOICES, blank=True,
                                     null=True)
    pais_publicacion= models.ForeignKey(UbigeoPais, on_delete=models.PROTECT)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)

    def delete(self, using=None, keep_parents=False):
        for au in self.adjuntocientifica_set.all():
            path = default_storage.path(au.ruta)
            if path:
                os.remove(path)
        super(Cientifica, self).delete()


class AdjuntoCientifica(BaseModel):
    nombre = models.CharField('Nombre del documento', max_length=200)
    ruta = models.TextField('Ruta del documento', max_length=500)
    tipo_obra = models.CharField('Tipo de obra', max_length=45, choices=TIPO_OBRA_CHOICES)
    tipo_documento_adjunto = models.CharField('Tipo de documento adjunto', max_length=45,
                                              choices=TIPO_DOC_ADJUNTO_CHOICES)
    cientifica = models.ForeignKey(Cientifica, on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        path = default_storage.path(self.ruta)
        if path:
            os.remove(path)
        super(AdjuntoCientifica, self).delete()
