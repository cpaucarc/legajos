from django.db import models

from apps.common.constants import COLEGIATURA_HABILITADO,COLEGIATURA_INHABILITADO,COLEGIATURA_ESTADO_CHOICES
from apps.common.models import AuditableModel, TimeStampedModel, Colegio

from apps.experiencia.models import Docente

class Colegiatura(AuditableModel, TimeStampedModel):
    colegio_id = models.ForeignKey(Colegio, on_delete=models.PROTECT, blank=True, null=True)
    sede = models.CharField('Sede', blank=True, null=True)
    codigo_colegiatura = models.CharField(max_length=15, verbose_name='Código')
    estado_colegiatura = models.BooleanField(verbose_name='Estado', choices=COLEGIATURA_ESTADO_CHOICES, default=COLEGIATURA_HABILITADO)
    docente_id = models.ForeignKey(Docente, on_delete=models.PROTECT, blank=True, null=True)