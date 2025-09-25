from datetime import timedelta
from django.core.management.base import BaseCommand
from entrenamiento.models import TrainingPlan, Workout, ExerciseLog
from django.utils import timezone
from io import BytesIO
import openpyxl
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Avg
from entrenamiento.models import Exercise
class Command(BaseCommand):
    help = 'Envía reportes semanales de progresos'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday() + 7)  # Inicio de semana pasada
        end_of_week = start_of_week + timedelta(days=6)
        plans = TrainingPlan.objects.filter(status='active')
        for plan in plans:
            workouts = plan.workouts.filter(date__range=[start_of_week, end_of_week])
            if not workouts.exists():
                continue
            # Analizar datos
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = f"Reporte Semanal - {plan.name}"
            ws.append(['Ejercicio', 'Avg Peso (kg)', 'Avg Reps', 'Avg RIR', 'Avg RPE', 'Consistencia (%)'])
            exercises = Exercise.objects.filter(workoutexercise__workout__in=workouts).distinct()
            total_workouts = workouts.count()
            completed_workouts = sum(1 for w in workouts if w.is_complete())
            consistency = (completed_workouts / total_workouts * 100) if total_workouts > 0 else 0
            for ex in exercises:
                logs = ExerciseLog.objects.filter(workout_exercise__exercise=ex, date_completed__range=[start_of_week, end_of_week])
                if logs.exists():
                    avg_weight = logs.aggregate(Avg('weight_lifted_kg'))['weight_lifted_kg__avg']
                    avg_reps = logs.aggregate(Avg('reps_completed'))['reps_completed__avg']
                    avg_rir = logs.aggregate(Avg('rir_actual'))['rir_actual__avg']
                    avg_rpe = logs.aggregate(Avg('rpe_actual'))['rpe_actual__avg']
                    ws.append([ex.name, avg_weight, avg_reps, avg_rir, avg_rpe, consistency])
            # Guardar y enviar
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            trainer_email = plan.trainer.email
            subject = f"Reporte Semanal: {plan.name} para {plan.client.username}"
            message = f"Adjunto el reporte semanal. Consistencia: {consistency}%"
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [trainer_email])
            email.attach(f'reporte_semanal_{start_of_week}.xlsx', output.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()
            self.stdout.write(self.style.SUCCESS(f'Reporte enviado para {plan.name}'))