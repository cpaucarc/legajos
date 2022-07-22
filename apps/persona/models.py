from django.core.validators import validate_email
from django.db import models

from apps.common.constants import DOCUMENT_TYPE_CHOICES, DOCUMENT_TYPE_DNI, SEXO_CHOICES, TIPO_PERSONA_CHOICES, \
    CATEGORIA_CHOICES, DEDICACION_CHOICES, TIPO_CONTRATO_CHOICES, COLEGIATURA_HABILITADO, COLEGIATURA_INHABILITADO, \
    COLEGIATURA_ESTADO_CHOICES
from apps.common.models import AuditableModel, TimeStampedModel, UbigeoPais, validate_ruc


class Facultad(models.Model):
    codigo = models.CharField('Código', max_length=45, unique=True)
    nombre = models.CharField('Nombre', max_length=250)

    def __str__(self):
        return '{nombre}'.format(nombre=self.nombre)


class Departamento(models.Model):
    codigo = models.CharField('Código', max_length=45, unique=True)
    nombre = models.CharField('Nombre', max_length=250)
    facultad = models.ForeignKey(Facultad, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return '{nombre}'.format(nombre=self.nombre)


class Persona(AuditableModel, TimeStampedModel):
    tipo_documento = models.CharField(
        max_length=2, verbose_name='Tipo de documento', choices=DOCUMENT_TYPE_CHOICES, default=DOCUMENT_TYPE_DNI)
    numero_documento = models.CharField(max_length=15, verbose_name='Número de documento')
    sexo = models.CharField('Sexo', choices=SEXO_CHOICES, max_length=2)
    nombres = models.CharField('Nombre(s)', max_length=120, blank=True, null=True)
    apellido_paterno = models.CharField('Apellido paterno', max_length=120, blank=True, null=True)
    apellido_materno = models.CharField('Apellido materno', max_length=120, blank=True, null=True)
    celular = models.CharField(max_length=50, null=True, blank=True)
    correo_personal = models.CharField(max_length=100, null=True, blank=True, validators=[validate_email])
    ruc = models.CharField(max_length=11, null=True, blank=True, validators=[validate_ruc], verbose_name='RUC')
    tipo_persona = models.CharField(max_length=25, choices=TIPO_PERSONA_CHOICES)
    facultad = models.ForeignKey(Facultad, on_delete=models.PROTECT, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, blank=True, null=True)
    ruta_foto = models.FileField(upload_to="foto", blank=True, null=True)
    resumen = models.TextField(max_length=1500, blank=True, null=True)
    es_activo = models.BooleanField(default=True)

    class Meta:
        unique_together = [('tipo_documento', 'numero_documento')]
        ordering = ['apellido_paterno']

    def __str__(self):
        return '{nombre_completo}'.format(nombre_completo=self.nombre_completo)

    @property
    def nombre_completo(self):
        return '{a_paterno} {a_materno} {nombres}'.format(
            nombres=self.nombres,
            a_paterno=self.apellido_paterno,
            a_materno=self.apellido_materno
        )

    @property
    def indenteficador_persona(self):
        return '{id}'.format(
            id=self.id
        )

    def get_default_password_and_username(self):
        if self.numero_documento:
            return self.numero_documento
        elif self.nombres:
            return self.nombres.lower().replace(' ', '')


class DatosGenerales(AuditableModel, TimeStampedModel):
    orcid = models.CharField('ORCID', max_length=45, null=True, blank=True)
    tipo_contrato = models.CharField('Tipo de contrato', max_length=45, choices=TIPO_CONTRATO_CHOICES)
    categoria = models.CharField('Categoria', max_length=45, choices=CATEGORIA_CHOICES)
    dedicacion = models.CharField('Dedicación', max_length=45, choices=DEDICACION_CHOICES)
    fecha_nacimiento = models.DateField('Fecha de nacimiento')
    nacionalidad = models.ForeignKey(UbigeoPais, on_delete=models.PROTECT)
    direccion = models.CharField('Dirección', max_length=200)
    correo_institucional = models.CharField(max_length=100, null=True, blank=True, validators=[validate_email])
    ubigeo_departamento = models.CharField('Departamento', max_length=2)
    ubigeo_provincia = models.CharField('Provincia', max_length=4)
    ubigeo_distrito = models.CharField('Distrito', max_length=6)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)


class Colegiatura(AuditableModel, TimeStampedModel):
    # colegio_profesional = models.ForeignKey(Colegio, on_delete=models.CASCADE, blank=True, null=True)
    colegio_profesional = models.CharField(verbose_name='Colegio profesional', max_length=5, blank=True, null=True)
    sede_colegio = models.CharField(verbose_name='Sede del colegio', max_length=200, blank=True, null=True)
    codigo_colegiado = models.CharField(verbose_name='Código del colegiado', max_length=15, blank=True, null=True)
    estado_colegiado = models.BooleanField(verbose_name='Estado del colegiado', choices=COLEGIATURA_ESTADO_CHOICES,
                                           default=COLEGIATURA_HABILITADO)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = [('codigo_colegiado')]
