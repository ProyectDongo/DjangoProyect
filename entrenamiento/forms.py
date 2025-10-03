from django import forms
from .models import TrainingPlan, Workout, WorkoutExercise, ExerciseLog, Warmup, Exercise
from core.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_file_size(value):
    if value.size > 500 * 1024 * 1024:  # 500MB
        raise ValidationError("El archivo es demasiado grande (máximo 500MB).")

class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ['name', 'client', 'start_date', 'end_date', 'notes']  # Agregado 'notes'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Plan de Volumen Muscular'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': 'Nombre del Plan',
            'client': 'Cliente',
            'start_date': 'Fecha de Inicio',
            'end_date': 'Fecha de Fin',
            'notes': 'Notas',
        }

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['week_number', 'day_of_week', 'title']
        widgets = {
            'week_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'day_of_week': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 7}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Entrenamiento de Piernas'}),
        }

class WorkoutExerciseForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all())
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'reps_target', 'rir_target', 'rpe_target', 'rest_period_seconds', 'notes', 'order', 'video_required']  # Agregado 'video_required'
        widgets = {
            'exercise': forms.Select(attrs={'class': 'form-select'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'reps_target': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 8-12'}),
            'rir_target': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'rpe_target': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'rest_period_seconds': forms.NumberInput(attrs={'class': 'form-control', 'min': 10}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'video_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ExerciseLogForm(forms.ModelForm):
    class Meta:
        model = ExerciseLog
        fields = ['weight_lifted_kg', 'reps_completed', 'rir_actual', 'rpe_actual', 'notes', 'video_log', 'status']
        labels = {
            'weight_lifted_kg': _("Peso Levantado (kg)"),
            'reps_completed': _("Repeticiones Completadas"),
            'rir_actual': _("RIR Real"),
            'rpe_actual': _("RPE Real"),
            'notes': _("Notas del Cliente"),
            'video_log': _("Video de Registro"),
            'status': _("Estado"),
        }
        widgets = {
            'weight_lifted_kg': forms.NumberInput(attrs={'class': 'form-control'}),
            'reps_completed': forms.NumberInput(attrs={'class': 'form-control'}),
            'rir_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'rpe_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'video_log': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['video_log'].validators.append(validate_file_size)
        self.fields['video_log'].validators.append(FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov']))  # Solo videos

class WarmupForm(forms.ModelForm):
    class Meta:
        model = Warmup
        fields = ['name', 'series_reps', 'notes', 'video_url', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Calentamiento de Movilidad'}),
            'series_reps': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2x15'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL del video'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }

class ClientCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'rut', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

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