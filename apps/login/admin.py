from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.login.models import User
from apps.persona.models import Persona


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'persona',
            'password'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['persona'].queryset = Persona.objects.filter(pk=self['persona'].value(), es_activo=True)


class MyUserCreationForm(UserCreationForm):
    persona = forms.ModelChoiceField(
        required=True,
        queryset=Persona.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self['persona'].value():
            self.fields['persona'].queryset = Persona.objects.filter(pk=self['persona'].value(), es_activo=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.persona.get_default_password_and_username()
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    model = User
    add_form_template = 'login/admin/add_form.html'
    change_form_template = 'login/admin/change_form.html'
    fieldsets = (
        (
            _('User Profile'),
            {
                'fields': ('persona', 'password')
             }
        ),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'persona', 'date_joined', 'last_login', 'is_superuser',)
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'persona', 'password1', 'password2', 'is_staff', 'is_active'
                )
            }
        ),
    )
    search_fields = ('username', 'persona')
