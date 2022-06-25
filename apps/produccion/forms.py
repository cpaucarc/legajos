from django import forms
from django.utils import timezone

from apps.common.constants import TIPO_CONGRESO_CHOICES
from apps.produccion.models import Cientifica


class CientificaForm(forms.ModelForm):
    tipo_congreso = forms.ChoiceField(
        label='Tipo de congreso',
        required=False,
        choices=TIPO_CONGRESO_CHOICES,
        widget=forms.RadioSelect()
    )
    fecha_publicacion = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                               attrs={'class': 'form-control input-sm',
                                                                      'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Cientifica
        fields = ('categoria_trabajo', 'tipo_obra', 'funcion', 'titulo', 'sub_titulo', 'revista',
                  'volumen', 'fasciculo', 'rango_paginas', 'fecha_publicacion', 'tipo_cita', 'cita', 'descripcion',
                  'orden_autoria', 'autor', 'pais_publicacion', 'tipo_congreso')

    def clean_fecha_publicacion(self):
        if self.cleaned_data.get('fecha_publicacion') and self.cleaned_data.get('fecha_publicacion') > timezone.now().date():  # noqa
            raise forms.ValidationError('La fecha de publicacion no puede ser mayor a la fecha actual')
        if not self.cleaned_data.get('fecha_publicacion'):
            raise forms.ValidationError('Debe registrar la fecha de publicacion')
        return self.cleaned_data.get('fecha_publicacion')
