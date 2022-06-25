from django import forms
from apps.idioma.models import Idioma


class IdiomaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Idioma
        fields = ('idioma', 'lectura', 'conversacion', 'escritura', 'forma_aprendizaje', 'es_lengua_materna')
