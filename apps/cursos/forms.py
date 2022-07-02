from django import forms

from apps.common.models import Institucion
from apps.cursos.models import Semestre


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
