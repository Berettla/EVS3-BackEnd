from django.conf import settings
from django.db import models


class Perfil(models.Model):
    """Datos complementarios del usuario (extiende django.contrib.auth.User)."""

    class Rol(models.TextChoices):
        CLIENTE = 'CLI', 'Cliente'
        ADMINISTRADOR = 'ADM', 'Administrador'

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
    )
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    rol = models.CharField(max_length=3, choices=Rol.choices, default=Rol.CLIENTE)

    def __str__(self):
        return f'{self.usuario.username} ({self.get_rol_display()})'