from django import forms
from django.utils.translation import gettext_lazy as _
from ejercicios.models import Exercise

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'video_url', 'muscle_group', 'equipment']
        labels = {
            'name': _("Nombre del Ejercicio"),
            'description': _("Descripción"),
            'video_url': _("URL del Video"),
            'muscle_group': _("Grupo Muscular"),
            'equipment': _("Equipamiento"),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'muscle_group': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment': forms.TextInput(attrs={'class': 'form-control'}),
        }