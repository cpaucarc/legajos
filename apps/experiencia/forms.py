from django import forms
from apps.experiencia.models import Laboral, Docente, AsesorTesis, EvaluadorProyecto


class LaboralForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                          attrs={'class': 'form-control input-sm', 'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                       attrs={'class': 'form-control input-sm', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Laboral
        fields = ('cargo', 'institucion', 'fecha_inicio', 'fecha_fin', 'trabaja_actualmente', 'descripcion_cargo')
        widgets = {
            'descripcion_cargo': forms.Textarea(attrs={'rows': 4, 'max_length': 100, 'class': 'form-control'}),
        }


class DocenteForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                          attrs={'class': 'form-control input-sm', 'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                       attrs={'class': 'form-control input-sm', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Docente
        fields = ('institucion', 'tipo_institucion', 'tipo_docente', 'fecha_inicio', 'fecha_fin', 'trabaja_actualmente',
                  'descripcion_cargo')
        widgets = {
            'descripcion_cargo': forms.Textarea(attrs={'rows': 4, 'max_length': 100, 'class': 'form-control'}),
        }


class AsesorTesisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = AsesorTesis
        fields = ('universidad', 'tesis', 'tesista', 'fecha_aceptacion_tesis', 'enlace_fuente_repositorio_academico')


class EvaluadorProyectoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = EvaluadorProyecto
        fields = ('experiencia', 'anio', 'pais', 'tipo_proyecto_formulado', 'metodologia_evaluacion',
                  'entidad_financiadora', 'nombre_concurso', 'url_concurso', 'presupuesto_proyecto')
