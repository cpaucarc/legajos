from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import PasswordInput


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'placeholder': 'Usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = 'autofocus'


class UsuarioPasswordChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label='Contraseña antigua', widget=PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Contraseña nueva', widget=PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(
        label='Contraseña nueva(confirmación)',
        widget=PasswordInput(attrs={'class': 'form-control'})
        )
