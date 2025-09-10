from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLES_CHOICES = [
        ("ENTRENADOR", "Entrenador"),
        ("CLIENTE", "Cliente"),
        ("NUTRICIONISTA", "nutricionista"),
    ]
    rut = models.CharField(max_length=12, unique=True)
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, verbose_name=_("Rol"))
    assigned_professional = models.ForeignKey(
        'self', related_name='clients', null=True, blank=True, on_delete=models.SET_NULL,
        verbose_name=_("Profesional Asignado")
    )
    bio = models.TextField(blank=True, verbose_name=_("Biografía"))
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name=_("Avatar"))

    def __str__(self):
        return f"{self.username} - {self.role}"