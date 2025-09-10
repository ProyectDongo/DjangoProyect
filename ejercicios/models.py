from django.db import models
from django.utils.translation import gettext_lazy as _

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Nombre del Ejercicio"))
    description = models.TextField(blank=True, verbose_name=_("Descripción"))
    video_url = models.URLField(blank=True, verbose_name=_("URL del Video"))
    muscle_group = models.CharField(max_length=100, blank=True, verbose_name=_("Grupo Muscular"))
    equipment = models.CharField(max_length=100, blank=True, verbose_name=_("Equipamiento"))

    def __str__(self):
        return self.name

class Warmup(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nombre del Calentamiento"))
    series_reps = models.CharField(max_length=50, verbose_name=_("Series/Reps"))
    notes = models.TextField(blank=True, verbose_name=_("Notas"))
    video_url = models.URLField(blank=True, verbose_name=_("URL del Video"))
    type = models.CharField(max_length=20, choices=[('inferior', 'Tren Inferior'), ('superior', 'Tren Superior')], verbose_name=_("Tipo"))

    def __str__(self):
        return self.name