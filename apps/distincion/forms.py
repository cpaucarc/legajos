from django import forms

from apps.distincion.models import Distincion


class DistincionForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control input-sm',
                                                                             'type': 'date'}))
    web_referencia = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Distincion
        fields = ('institucion', 'distincion', 'descripcion', 'pais', 'web_referencia', 'fecha')
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5, 'max_length': 600, 'class': 'form-control'}),
        }
