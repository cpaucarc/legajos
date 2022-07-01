from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.common.models import AuditableModel, TimeStampedModel
from apps.persona.models import Persona


class User(AbstractUser, AuditableModel, TimeStampedModel):
    # persona = models.ForeignKey(Persona, on_delete=models.PROTECT, blank=True, null=True)
    persona = models.OneToOneField(Persona, on_delete=models.PROTECT, blank=True, null=True)
    PERSONA_FIELD = 'persona'

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        # fields = ["id", "password", "last_login", "is_superuser", "username",
        #     "first_name", "last_name", "email", "is_staff", "is_active", "date_joined",
        #     "creado_por", "modificado_por", "fecha_creacion", "fecha_modificacion", "persona_id"]

    def __str__(self):
        return self.username
