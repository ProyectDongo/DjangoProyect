from django.db import models
from django.conf import settings  
from django.utils.translation import gettext_lazy as _
from datetime import timedelta  



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
    



class TrainingPlan(models.Model):
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Cambiado de User
        related_name='created_plans',
        on_delete=models.CASCADE,
        verbose_name=_("Entrenador")
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Cambiado de User
        related_name='assigned_plans',
        on_delete=models.CASCADE,
        verbose_name=_("Cliente")
    )
    name = models.CharField(max_length=200, verbose_name=_("Nombre del Plan"))
    start_date = models.DateField(verbose_name=_("Fecha de Inicio"))
    end_date = models.DateField(verbose_name=_("Fecha de Fin"))
    status = models.CharField(max_length=20, default='active', choices=[('active', 'Activo'), ('completed', 'Completado')], verbose_name=_("Estado"))
    notes = models.TextField(blank=True, verbose_name=_("Notas"))
    
    def __str__(self):
        return f"Plan '{self.name}' para {self.client.username}"
    



class Workout(models.Model):
    plan = models.ForeignKey(TrainingPlan, related_name='workouts', on_delete=models.CASCADE, verbose_name=_("Plan"))
    week_number = models.PositiveIntegerField(verbose_name=_("Número de Semana"))
    day_of_week = models.PositiveIntegerField(verbose_name=_("Día de la Semana (1=Lunes)"))
    title = models.CharField(max_length=200, verbose_name=_("Título del Entrenamiento"))
    date = models.DateField(null=True, blank=True, verbose_name=_("Fecha del Entrenamiento"))  # CAMBIO: Campo agregado

    def __str__(self):
        return f"{self.plan.name} - Semana {self.week_number}, Día {self.day_of_week}: {self.title}"

    def save(self, *args, **kwargs):
        # CAMBIO: Calcular fecha automáticamente si no está seteada
        if not self.date and self.plan and self.plan.start_date:
            delta_days = (self.week_number - 1) * 7 + (self.day_of_week - 1)
            self.date = self.plan.start_date + timedelta(days=delta_days)
        super().save(*args, **kwargs)




class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, related_name='exercises', on_delete=models.CASCADE, verbose_name=_("Entrenamiento"))
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT, verbose_name=_("Ejercicio"))
    sets = models.PositiveIntegerField(verbose_name=_("Series"))
    reps_target = models.CharField(max_length=50, verbose_name=_("Repeticiones Objetivo"))
    rir_target = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("RIR Objetivo"))
    rpe_target = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("RPE Objetivo"))
    rest_period_seconds = models.PositiveIntegerField(default=60, verbose_name=_("Descanso (segundos)"))
    notes = models.TextField(blank=True, verbose_name=_("Notas"))
    order = models.PositiveIntegerField(default=1, verbose_name=_("Orden en el Workout"))

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.sets}x{self.reps_target} de {self.exercise.name}"
    
    def get_last_log(self):
        return ExerciseLog.objects.filter(workout_exercise=self).order_by('-date_completed').first()

class ExerciseLog(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completado'),
        ('half', 'A Medias'),
        ('not_completed', 'No Completado'),
    ]
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Cliente")
    )
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, verbose_name=_("Ejercicio del Plan"))
    date_completed = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de Completado"))
    weight_lifted_kg = models.FloatField(verbose_name=_("Peso Levantado (kg)"))
    reps_completed = models.PositiveIntegerField(verbose_name=_("Repeticiones Completadas"))
    rir_actual = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("RIR Real"))
    rpe_actual = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("RPE Real"))
    notes = models.TextField(blank=True, verbose_name=_("Notas del Cliente"))
    video_log = models.FileField(
        upload_to='logs/videos/',
        null=True,
        blank=True,
        verbose_name=_("Video de Registro")
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name=_("Estado"))

    def __str__(self):
        return f"Registro de {self.client.username} para {self.workout_exercise.exercise.name} el {self.date_completed.strftime('%Y-%m-%d')}"