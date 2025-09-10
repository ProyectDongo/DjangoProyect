from django import forms
from .models import TrainingPlan, Workout, WorkoutExercise, ExerciseLog
from ejercicios.models import Exercise, Warmup
from core.models import User

class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ['name', 'client', 'start_date', 'end_date']
        
        # Con widgets, personalizamos cómo se muestra cada campo en el HTML.
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: Plan de Volumen Muscular'
            }),
            'client': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date', # Esto activa el calendario del navegador.
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date', # Y aquí también.
                'class': 'form-control'
            }),
        }

        # Opcional: Para ordenar las etiquetas en español si no lo están ya
        labels = {
            'name': 'Nombre del Plan',
            'client': 'Cliente',
            'start_date': 'Fecha de Inicio',
            'end_date': 'Fecha de Fin',
        }


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['week_number', 'day_of_week', 'title']

class WorkoutExerciseForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all())
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'reps_target', 'rir_target', 'rpe_target', 'rest_period_seconds', 'notes', 'order']

class ExerciseLogForm(forms.ModelForm):
    class Meta:
        model = ExerciseLog
        fields = ['weight_lifted_kg', 'reps_completed', 'rir_actual', 'rpe_actual', 'notes', 'video_log', 'status']

class WarmupForm(forms.ModelForm):
    class Meta:
        model = Warmup
        fields = ['name', 'series_reps', 'notes', 'video_url', 'type']


class ClientCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'rut', 'first_name', 'last_name' ,'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }