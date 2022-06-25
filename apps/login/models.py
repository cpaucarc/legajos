from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.common.models import AuditableModel, TimeStampedModel
from apps.persona.models import Persona


class User(AbstractUser, AuditableModel, TimeStampedModel):
    persona = models.OneToOneField(Persona, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username
