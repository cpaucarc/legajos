from django.db import models

from apps.common.constants import NIVEL_IDIOMA_CHOICES, FORMA_APRENDIZAJE_CHOICES
from apps.common.models import CatalogoIdiomas, BaseModel
from apps.persona.models import Persona


class Idioma(BaseModel):
    idioma = models.ForeignKey(CatalogoIdiomas, on_delete=models.PROTECT)
    lectura = models.CharField(choices=NIVEL_IDIOMA_CHOICES, max_length=45)
    conversacion = models.CharField(choices=NIVEL_IDIOMA_CHOICES, max_length=45)
    escritura = models.CharField(choices=NIVEL_IDIOMA_CHOICES, max_length=45)
    forma_aprendizaje = models.CharField(choices=FORMA_APRENDIZAJE_CHOICES, max_length=45)
    es_lengua_materna = models.BooleanField(default=False)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)
