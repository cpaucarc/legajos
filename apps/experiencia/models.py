import os
from django.core.files.storage import default_storage
from django.db import models

from apps.common.constants import (TIPO_INSTITUCION_CHOICES, TIPO_DOCENTE_CHOICES,
                                   TIPO_TESIS_CHOICES, TIPO_EXPERIENCIA_PROYECTO_CHOICES, PROYECTO_FORMULADO_CHOICES,
                                   METODOLOGIA_EVALUACION_CHOICES)
from apps.common.models import Institucion, UbigeoPais, BaseModel
from apps.persona.models import Persona


class Laboral(BaseModel):
    cargo = models.CharField('Cargo', max_length=100)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT)
    fecha_inicio = models.DateField('Fecha inicio')
    fecha_fin = models.DateField('Fecha fin', blank=True, null=True)
    trabaja_actualmente = models.BooleanField(default=False)
    descripcion_cargo = models.CharField('Descripcion del cargo', max_length=250)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)


class AdjuntoLaboral(BaseModel):
    nombre = models.CharField('Nombre del documento', max_length=200)
    ruta = models.TextField('Ruta del documento', max_length=500)
    laboral = models.ForeignKey(Laboral, on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        path = default_storage.path(self.ruta)
        if path:
            os.remove(path)
        super(AdjuntoLaboral, self).delete()


class Docente(BaseModel):
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT)
    tipo_institucion = models.CharField(max_length=45, choices=TIPO_INSTITUCION_CHOICES)
    tipo_docente = models.CharField(max_length=70, choices=TIPO_DOCENTE_CHOICES, blank=True, null=True)
    fecha_inicio = models.DateField('Fecha inicio')
    fecha_fin = models.DateField('Fecha fin', blank=True, null=True)
    trabaja_actualmente = models.BooleanField(default=False)
    descripcion_cargo = models.CharField('Descripcion del cargo', max_length=250)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)


class AdjuntoDocente(BaseModel):
    nombre = models.CharField('Nombre del documento', max_length=200)
    ruta = models.TextField('Ruta del documento', max_length=500)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        path = default_storage.path(self.ruta)
        if path:
            os.remove(path)
        super(AdjuntoDocente, self).delete()


class AsesorTesis(models.Model):
    universidad = models.ForeignKey(Institucion, on_delete=models.PROTECT)
    tesis = models.CharField(max_length=45, choices=TIPO_TESIS_CHOICES)
    tesista = models.CharField('Tesista', max_length=200)
    fecha_aceptacion_tesis = models.DateField('Fecha de aceptación de la tesis')
    enlace_fuente_repositorio_academico = models.CharField('Enlace de Fuente del repositorio académico', max_length=250,
                                                           blank=True, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)


class AdjuntoAsesorTesis(BaseModel):
    nombre = models.CharField('Nombre del documento', max_length=200)
    ruta = models.TextField('Ruta del documento', max_length=500)
    asesor_tesis = models.ForeignKey(AsesorTesis, on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        path = default_storage.path(self.ruta)
        if path:
            os.remove(path)
        super(AdjuntoAsesorTesis, self).delete()


class EvaluadorProyecto(BaseModel):
    experiencia = models.CharField(max_length=45, choices=TIPO_EXPERIENCIA_PROYECTO_CHOICES, blank=True, null=True)
    anio = models.CharField('Año del proyecto', max_length=4, blank=True, null=True)
    pais = models.ForeignKey(UbigeoPais, on_delete=models.PROTECT, blank=True, null=True)
    tipo_proyecto_formulado = models.CharField('Tipo de proyecto formulado/evaluado', max_length=45,
                                               choices=PROYECTO_FORMULADO_CHOICES)
    metodologia_evaluacion = models.CharField('Metodología de evaluación', max_length=45, blank=True, null=True,
                                              choices=METODOLOGIA_EVALUACION_CHOICES)
    entidad_financiadora = models.ForeignKey(Institucion, on_delete=models.PROTECT, blank=True, null=True)
    nombre_concurso = models.CharField('Nombre del concurso', max_length=250)
    url_concurso = models.CharField('Url del concurso', max_length=250, blank=True, null=True)
    presupuesto_proyecto = models.DecimalField('Presupuesto total del proyecto formulado/evaluado', decimal_places=2,
                                               max_digits=10, blank=True, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)


class AdjuntoEvaluadorProyecto(BaseModel):
    nombre = models.CharField('Nombre del documento', max_length=200)
    ruta = models.TextField('Ruta del documento', max_length=500)
    evaluador_proyecto = models.ForeignKey(EvaluadorProyecto, on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        path = default_storage.path(self.ruta)
        if path:
            os.remove(path)
        super(AdjuntoEvaluadorProyecto, self).delete()
