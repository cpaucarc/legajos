from django import forms
from django.forms import inlineformset_factory

from apps.common.constants import DOCUMENT_TYPE_DNI, DOCUMENT_TYPE_CHOICES1, ID_UBIGEO_PERU, COLEGIATURA_HABILITADO, \
    COLEGIATURA_INHABILITADO, COLEGIATURA_ESTADO_CHOICES
from apps.common.models import UbigeoDepartamento, UbigeoProvincia, UbigeoDistrito, Colegio
from apps.persona.models import Persona, DatosGenerales, Departamento, Colegiatura
from django.utils import timezone


class PersonaForm(forms.ModelForm):
    tipo_documento = forms.ChoiceField(label='Tipo de documento', choices=DOCUMENT_TYPE_CHOICES1,
                                       initial=DOCUMENT_TYPE_DNI,
                                       widget=forms.Select(attrs={'class': 'form-control form-control-lg'})
                                       )
    apellido_paterno = forms.CharField(required=True)
    nombres = forms.CharField(required=True)
    celular = forms.CharField(required=True)
    ruc = forms.CharField(required=False)
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.none(), required=False)
    ruta_foto = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control input-sm'}))

    colegio_profesional_select = forms.ModelChoiceField(queryset=Colegio.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.data.get('facultad'):
            self.fields['departamento'].queryset = Departamento.objects.filter(id=self.data.get('facultad'))
        if self['facultad'].value():
            self.fields['departamento'].queryset = Departamento.objects.filter(facultad_id=self['facultad'].value())
            self.fields['departamento'].initial = self['departamento'].value()

        self.fields['colegio_profesional_select'].queryset = Colegio.objects.all()
        self.fields['colegio_profesional_select'].label = "Colegio Profesional"

    sede_colegio_input = forms.CharField(label='Sede del Colegio Profesional', required=False)
    codigo_colegiado_input = forms.CharField(label='Código de Colegiado', required=False)
    estado_colegiado_select = forms.ChoiceField(label='Estado del Colegiado', required=False,
                                                choices=COLEGIATURA_ESTADO_CHOICES,
                                                initial=COLEGIATURA_HABILITADO,
                                                widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Persona
        fields = (
            'tipo_documento', 'numero_documento', 'sexo', 'nombres', 'apellido_paterno', 'apellido_materno',
            'celular', 'correo_personal', 'ruc', 'tipo_persona', 'departamento', 'facultad', 'resumen'
        )
        widgets = {
            'resumen': forms.Textarea(attrs={'rows': 3, 'max_length': 1500, 'class': 'form-control'}),
        }

    def clean_ruc(self):
        if len(self.cleaned_data.get('ruc')) != 11 and len(self.cleaned_data.get('ruc')) != 0:  # noqa
            raise forms.ValidationError('El N° RUC debe tener 11 digitos')
        if not str(self.cleaned_data.get('ruc')).startswith('10') and not str(self.cleaned_data.get(
                'ruc')).startswith('20') and not len(self.cleaned_data.get('ruc')) == 0:
            raise forms.ValidationError('El N°RUC debe comenzar con 10 o 20')
        return self.cleaned_data.get('ruc')


class DatosGeneralesForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                              attrs={'class': 'form-control input-sm', 'type': 'date',
                                                                     'min': ''}),
                                       label='Fecha de nacimiento')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ubigeo_departamento'] = forms.ChoiceField(
            label='Departamento',
            choices=[('', '---------')] + get_departamentos(),
            widget=forms.Select(attrs={'class': 'form-control form-control-lg'}))

        self.fields['ubigeo_provincia'] = forms.ChoiceField(
            label='Provincias',
            choices=[('', '---------')] + get_provincias(
                self['ubigeo_departamento'].value()),
            widget=forms.Select(attrs={'class': 'form-control form-control-lg'}))

        self.fields['ubigeo_distrito'] = forms.ChoiceField(
            label='Distrito',
            choices=[('', '---------')] + get_distritos(
                self['ubigeo_departamento'].value(),
                self['ubigeo_provincia'].value()),
            widget=forms.Select(attrs={'class': 'form-control form-control-lg'}))

    class Meta:
        model = DatosGenerales
        fields = (
            'fecha_nacimiento', 'nacionalidad', 'tipo_contrato', 'categoria', 'dedicacion',
            'correo_institucional', 'ubigeo_departamento', 'ubigeo_provincia', 'ubigeo_distrito'
        )

    def clean_fecha_nacimiento(self):
        if self.cleaned_data.get('fecha_nacimiento') and self.cleaned_data.get(
                'fecha_nacimiento') > timezone.now().date():  # noqa
            raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
        if not self.cleaned_data.get('fecha_nacimiento'):
            raise forms.ValidationError('Debe registrar fecha de nacimiento')
        return self.cleaned_data.get('fecha_nacimiento')

class ColeForm(forms.ModelForm):
    colegio_profesional = forms.ModelChoiceField(queryset=Colegio.objects.filter().order_by('name'), widget=forms.Select())
    sede_colegio = forms.CharField(label='Sede del Colegio Profesional', widget=forms.TextInput())
    codigo_colegiado = forms.CharField(label='Código de Colegiado', widget=forms.TextInput())
    estado_colegiado = forms.ChoiceField(label='Estado del Colegiado', choices=COLEGIATURA_ESTADO_CHOICES, initial=COLEGIATURA_HABILITADO, widget=forms.Select())

    class Meta:
        model = Colegiatura
        fields = ('colegio_profesional', 'sede_colegio', 'codigo_colegiado', 'estado_colegiado')


def get_departamentos(cod_dep=None):
    if cod_dep:
        departamentos = UbigeoDepartamento.objects.filter(
            cod_ubigeo_inei_departamento=cod_dep
        ).values_list('cod_ubigeo_inei_departamento', 'ubigeo_departamento')
    else:
        departamentos = UbigeoDepartamento.objects.filter(
            pais__cod_ubigeo_inei_pais=ID_UBIGEO_PERU
        ).values_list('cod_ubigeo_inei_departamento', 'ubigeo_departamento')
    return list(departamentos)


def get_provincias(dep_id):
    provincias = UbigeoProvincia.objects.filter(
        departamento__cod_ubigeo_inei_departamento=dep_id
    ).values_list('cod_ubigeo_inei_provincia', 'ubigeo_provincia')
    return list(provincias)


def get_distritos(dep_id, prov_id):
    distritos = UbigeoDistrito.objects.filter(
        departamento__cod_ubigeo_inei_departamento=dep_id, provincia__cod_ubigeo_inei_provincia=prov_id
    ).values_list('cod_ubigeo_inei_distrito', 'ubigeo_distrito')
    return list(distritos)


def get_deptos_academicos(fac_id):
    deptos = Departamento.objects.filter(
        facultad_id=fac_id
    ).values_list('id', 'nombre')
    return list(deptos)


def get_colegios(col_id=None):
    col_list = ['id', 'name']
    if col_id:
        colegios = Colegio.objects.filter(
            id=col_id
        ).values_list(*col_list)
    else:
        colegios = Colegio.objects.all().values_list(*col_list)
    return list(colegios)


def get_colegio_name(col_id):
    if col_id:
        # return Colegio.objects.filter(id=col_id)
        return Colegio.objects.only('name').get(id=col_id).name
    else:
        return None


def get_estado_colegiado(status):
    if status:
        return 'Habilitado'
    else:
        return 'Inhabilitado'


class ExportarCVForm(forms.Form):
    datos_personales = forms.CharField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'style': 'cursor:pointer;'}))
    experiencia_laboral = forms.CharField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'style': 'cursor:pointer;'}))
    formacion_academica = forms.CharField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'style': 'cursor:pointer;'}))
    idiomas = forms.CharField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'style': 'cursor:pointer;'}))
    produccion_cientifica = forms.CharField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'style': 'cursor:pointer;'}))
    premios = forms.CharField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'style': 'cursor:pointer;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ColegiaturaForm(forms.ModelForm):
    colegio_profesional = forms.IntegerField(widget=forms.HiddenInput(attrs={'class': 'colegio-profesional-id'}))
    colegio_profesional_persona = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': True, 'class': 'colegio-profesional-persona'})
    )
    sede_colegio = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'sede-colegio-id'}))
    sede_colegio_persona = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': True, 'class': 'sede-colegio-persona'})
    )
    codigo_colegiado = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'codigo-colegiado-id'}))
    codigo_colegiado_persona = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': True, 'class': 'codigo-colegiado-persona'})
    )
    estado_colegiado = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'estado-colegiado-id'}))
    estado_colegiado_persona = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': True, 'class': 'estado-colegiado-persona'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Colegiatura
        fields = (
            'colegio_profesional', 'sede_colegio', 'codigo_colegiado', 'estado_colegiado'
        )


ColegiaturaFormset = inlineformset_factory(Persona, Colegiatura, form=ColegiaturaForm, can_delete=True, extra=0)
