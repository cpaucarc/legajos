from django import forms

from apps.common.models import Institucion
from apps.cursos.models import Semestre, ResponsabilidadSocial


class CursosCrearForm(forms.ModelForm):
    attrs = {'class': 'form-control-sm'}

    escuela = forms.CharField(widget=forms.TextInput(attrs))
    institucion = forms.ModelChoiceField(queryset=Institucion.objects.filter(name__icontains="Univ").order_by('name'),
                                         widget=forms.Select(attrs))
    semestre = forms.ModelChoiceField(queryset=Semestre.objects.all().order_by('nombre'), widget=forms.Select(attrs))
    curso = forms.CharField(widget=forms.TextInput(attrs))

    class Meta:
        model = Semestre
        fields = ('institucion', 'escuela', 'semestre', 'curso')

class RsuCrearForm(forms.ModelForm):
    attrs = {'class': 'form-control-sm'}

    titulo = forms.CharField(widget=forms.TextInput(attrs))
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows':2}), required=False)
    fecha_inicio = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control input-sm', 'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control input-sm', 'type': 'date'}))
    # fecha_fin = models.DateField('Fecha de fin')
    lugar = forms.CharField(widget=forms.TextInput(attrs))
    empresa = forms.CharField(widget=forms.TextInput(attrs), required=False)
    ruc = forms.CharField(widget=forms.TextInput(attrs), required=False)

    class Meta:
        model = ResponsabilidadSocial
        fields = ('titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'lugar', 'empresa', 'ruc')
