from django import forms
from django.utils import timezone

from apps.formacion.models import Universitaria, Tecnico, Complementaria


class UniversitariaForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                          attrs={'class': 'form-control input-sm', 'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                       attrs={'class': 'form-control input-sm', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Universitaria
        fields = ('grado_obtenido', 'nombre_grado', 'centro_estudios', 'facultad', 'fecha_inicio', 'fecha_fin',
                  'pais_estudios')

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                self.add_error('fecha_fin', 'La fecha fin no puede ser menor a la fecha de inicio')
            if fecha_inicio > timezone.now().date():
                self.add_error('fecha_inicio', 'La fecha inicio no puede ser mayor a la fecha actual')
            if fecha_fin > timezone.now().date():
                self.add_error('fecha_fin', 'La fecha fin no puede ser mayor a la fecha actual')


class TecnicoForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                          attrs={'class': 'form-control input-sm', 'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                       attrs={'class': 'form-control input-sm', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Tecnico
        fields = ('centro_estudios', 'nombre_carrera', 'fecha_inicio', 'fecha_fin')

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                self.add_error('fecha_fin', 'La fecha fin no puede ser menor a la fecha de inicio')
            if fecha_inicio > timezone.now().date():
                self.add_error('fecha_inicio', 'La fecha inicio no puede ser mayor a la fecha actual')
            if fecha_fin > timezone.now().date():
                self.add_error('fecha_fin', 'La fecha fin no puede ser mayor a la fecha actual')


class ComplementariaForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                          attrs={'class': 'form-control input-sm', 'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                       attrs={'class': 'form-control input-sm', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Complementaria
        fields = ('capacitacion_complementaria', 'centro_estudios', 'pais_estudios', 'frecuencia', 'cantidad',
                  'fecha_inicio', 'fecha_fin')

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                self.add_error('fecha_fin', 'La fecha fin no puede ser menor a la fecha de inicio')
            if fecha_inicio > timezone.now().date():
                self.add_error('fecha_inicio', 'La fecha inicio no puede ser mayor a la fecha actual')
            if fecha_fin > timezone.now().date():
                self.add_error('fecha_fin', 'La fecha fin no puede ser mayor a la fecha actual')