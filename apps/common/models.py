from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class AuditableModel(models.Model):
    creado_por = models.CharField('creado por', max_length=20, editable=False, blank=True, null=True)
    modificado_por = models.CharField('modificado por', max_length=20, editable=False, blank=True, null=True)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    fecha_creacion = models.DateTimeField('fecha de creación', auto_now_add=True, editable=False, blank=True, null=True) # noqa
    fecha_modificacion = models.DateTimeField('fecha de modificación', auto_now=True, editable=False)

    class Meta:
        abstract = True


class BaseModel(AuditableModel, TimeStampedModel):

    class Meta:
        abstract = True


class UbigeoPais(models.Model):
    alpha3 = models.CharField(max_length=3, null=True, blank=True)
    alpha2 = models.CharField(max_length=2, null=True, blank=True)
    cod_ubigeo_reniec_pais = models.CharField(
        'Código Ubigeo Pais - RENIEC', max_length=3,
        validators=[
            RegexValidator(regex='^[0-9]{1,3}$', message='Numero de 1 o 3 digitos'),
        ], null=False, blank=False)
    cod_ubigeo_inei_pais = models.CharField(
        'Código Ubigeo Pais - INEI', max_length=3,
        validators=[
            RegexValidator(regex='^[0-9]{1,3}$', message='Numero de 1 o 3 digitos'),
        ], null=False, blank=False)
    ubigeo_pais = models.CharField('Nombre Ubigeo Pais', max_length=100, null=False, blank=False)
    cod_telefono = models.CharField('Código Teléfono', max_length=10, null=True, blank=True)

    def __str__(self):
        return self.ubigeo_pais

    class Meta:
        verbose_name_plural = '2. Ubigeo Paises'


class UbigeoDepartamento(models.Model):
    cod_ubigeo_reniec_departamento = models.CharField(
        'Código Ubigeo Departamento - RENIEC', max_length=2,
        validators=[
            RegexValidator(
                regex='^[0-9]{2}$',
                message='Numero de 2 digitos',
            ),
        ], null=False, blank=False)
    cod_ubigeo_inei_departamento = models.CharField(
        'Código Ubigeo Departamento - INEI', max_length=2,
        validators=[
            RegexValidator(
                regex='^[0-9]{2}$',
                message='Numero de 2 digitos',
            ),
        ], null=False, blank=False)
    ubigeo_departamento = models.CharField(
        'Nombre Ubigeo Departamento', max_length=100, null=False, blank=False)
    pais = models.ForeignKey(
        UbigeoPais,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_pais')

    def __str__(self):
        return self.ubigeo_departamento

    class Meta:
        verbose_name_plural = '3. Ubigeo Departamentos'


class UbigeoProvincia(models.Model):
    cod_ubigeo_reniec_provincia = models.CharField(
        'Código Ubigeo Provincia - RENIEC', max_length=4,
        validators=[
            RegexValidator(
                regex='^[0-9]{4}$',
                message='Numero de 4 digitos',
            ),
        ], null=False, blank=False)
    cod_ubigeo_inei_provincia = models.CharField(
        'Código Ubigeo Provincia - INEI', max_length=4,
        validators=[
            RegexValidator(
                regex='^[0-9]{4}$',
                message='Numero de 4 digitos',
            ),
        ], null=False, blank=False)
    ubigeo_provincia = models.CharField(
        'Nombre Ubigeo Provincia', max_length=100, null=False, blank=False)
    pais = models.ForeignKey(
        UbigeoPais,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_pais')
    departamento = models.ForeignKey(
        UbigeoDepartamento,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_departamento')

    def __str__(self):
        return self.ubigeo_provincia

    class Meta:
        verbose_name_plural = '4. Ubigeo Provincias'

    @property
    def ubigeo_departamento(self):
        return self.departamento.ubigeo_departamento


class UbigeoDistrito(models.Model):
    cod_ubigeo_reniec_distrito = models.CharField(
        'Código Ubigeo Distrito - RENIEC', max_length=6,
        validators=[
            RegexValidator(
                regex='^[0-9]{6}$',
                message='Numero de 6 digitos',
            ),
        ], null=False, blank=False)
    cod_ubigeo_inei_distrito = models.CharField(
        'Código Ubigeo Distrito - INEI', max_length=6,
        validators=[
            RegexValidator(
                regex='^[0-9]{6}$',
                message='Numero de 6 digitos',
            ),
        ], null=False, blank=False)
    ubigeo_distrito = models.CharField(
        'Nombre Ubigeo Distrito', max_length=100, null=False, blank=False)
    pais = models.ForeignKey(
        UbigeoPais,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_pais')
    departamento = models.ForeignKey(
        UbigeoDepartamento,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_departamento')
    provincia = models.ForeignKey(
        UbigeoProvincia,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_provincia')
    l_inf = models.CharField(max_length=15, null=True, blank=True)
    l_sup = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.ubigeo_distrito

    class Meta:
        verbose_name_plural = '5. Ubigeo Distritos'

    @property
    def ubigeo_departamento(self):
        return self.departamento.ubigeo_departamento

    @property
    def ubigeo_provincia(self):
        return self.provincia.ubigeo_provincia


def validate_ruc(value):
    if len(value) != 11:
        raise ValidationError(
            _('El N°RUC debe tener 11 digitos'),  # noqa
            params={'value': value},
        )
    if not str(value).startswith('10') and not str(value).startswith('20'):
        raise ValidationError(
            _('El N°RUC debe comenzar con 10 o 20')  # noqa
        )


class Institucion(models.Model):
    ruc = models.CharField(max_length=11, validators=[validate_ruc])
    name = models.CharField(max_length=200)

    def __str__(self):
        return '{ruc}-{name}'.format(ruc=self.ruc, name=self.name)


class CatalogoIdiomas(models.Model):
    codigo = models.CharField(max_length=6)
    descripcion = models.CharField(max_length=45)

    def __str__(self):
        return self.descripcion
