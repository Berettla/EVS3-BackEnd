import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil


class RegistroForm(UserCreationForm):
    """Registro de cliente: usuario de Django + datos del Perfil."""
    first_name = forms.CharField(max_length=50, label='Nombres')
    last_name = forms.CharField(max_length=50, label='Apellidos')
    email = forms.EmailField(label='Correo electrónico')
    rut = forms.CharField(max_length=12, label='RUT', help_text='Formato: 12.345.678-5')
    telefono = forms.CharField(max_length=15, required=False, label='Teléfono')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    field_order = ['username', 'first_name', 'last_name', 'email', 'rut', 'telefono', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def clean_rut(self):
        rut = self.cleaned_data['rut'].strip().upper()
        if not re.match(r'^\d{1,2}\.\d{3}\.\d{3}-[\dK]$', rut):
            raise forms.ValidationError('Ingresa el RUT con puntos y guion, ej: 12.345.678-5.')
        if Perfil.objects.filter(rut=rut).exists():
            raise forms.ValidationError('Ya existe un usuario registrado con este RUT.')
        return rut

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Perfil.objects.create(
                usuario=user,
                rut=self.cleaned_data['rut'],
                telefono=self.cleaned_data['telefono'],
                rol=Perfil.Rol.CLIENTE,
            )
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'