from django import forms

from apps.common.constants import DOCUMENT_TYPE_DNI, DOCUMENT_TYPE_CHOICES1, ID_UBIGEO_PERU
from apps.common.models import UbigeoDepartamento, UbigeoProvincia, UbigeoDistrito
from apps.persona.models import Persona, DatosGenerales, Departamento
from django.utils import timezone


class PersonaForm(forms.ModelForm):
    tipo_documento = forms.ChoiceField(label='Tipo de documento', choices=DOCUMENT_TYPE_CHOICES1,
                                       initial=DOCUMENT_TYPE_DNI,
                                       widget=forms.Select(attrs={'class': 'form-control form-control-lg'})
                                       )
    apellido_paterno = forms.CharField(required=True)
    nombres = forms.CharField(required=True)
    celular = forms.CharField(required=True)
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.none(), required=False)
    ruta_foto = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control input-sm'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data.get('facultad'):
            self.fields['departamento'].queryset = Departamento.objects.filter(id=self.data.get('facultad'))
        if self['facultad'].value():
            self.fields['departamento'].queryset = Departamento.objects.filter(id=self['facultad'].value())
            self.fields['departamento'].initial = self['departamento'].value()

    class Meta:
        model = Persona
        fields = (
            'tipo_documento', 'numero_documento', 'sexo', 'nombres', 'apellido_paterno', 'apellido_materno',
            'celular', 'correo_personal', 'tipo_persona', 'departamento', 'facultad', 'resumen'
        )
        widgets = {
            'resumen': forms.Textarea(attrs={'rows': 3, 'max_length': 1500, 'class': 'form-control'}),
        }


class DatosGeneralesForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                              attrs={'class': 'form-control input-sm', 'type': 'date', 'min': ''}),
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
        if self.cleaned_data.get('fecha_nacimiento') and self.cleaned_data.get('fecha_nacimiento') > timezone.now().date():  # noqa
            raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
        if not self.cleaned_data.get('fecha_nacimiento'):
            raise forms.ValidationError('Debe registrar fecha de nacimiento')
        return self.cleaned_data.get('fecha_nacimiento')


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
