
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import ExerciseLog, TrainingPlan, Workout, WorkoutExercise
from ejercicios.models import Warmup
from .forms import TrainingPlanForm, WorkoutForm, WorkoutExerciseForm, ExerciseLogForm, WarmupForm
from core.models import User
from django.utils import timezone  
from datetime import timedelta     
from django.contrib import messages
from .forms import ClientCreationForm
from django.utils.crypto import get_random_string


@login_required
def trainer_dashboard(request):
    if request.user.role != 'ENTRENADOR':
        return redirect('inicio')
    plans = TrainingPlan.objects.filter(trainer=request.user)
    active_plans_count = plans.filter(status='active').count()
    clients = User.objects.filter(role='CLIENTE', assigned_professional=request.user)
    clients_count = clients.count()
    weekly_sessions = Workout.objects.filter(
        plan__in=plans,
        date__range=[timezone.now().date(), timezone.now().date() + timedelta(days=7)]
    ).exclude(date__isnull=True).count()
    exercises_count = WorkoutExercise.objects.filter(workout__plan__in=plans).count()
    warmups = Warmup.objects.all()
    warmups_upper_body = warmups.filter(type='superior')
    warmups_lower_body = warmups.filter(type='inferior')
    # Calcular datos para clientes
    for client in clients:
        client.active_plans = client.assigned_plans.filter(status='active').count()
        last_log = ExerciseLog.objects.filter(client=client).order_by('-date_completed').first()
        client.last_session = last_log.date_completed if last_log else None
    context = {
        'plans': plans,
        'active_plans_count': active_plans_count,
        'clients_count': clients_count,
        'weekly_sessions': weekly_sessions,
        'exercises_count': exercises_count,
        'clients': clients,
        'warmups': {
            'upper_body': warmups_upper_body,
            'lower_body': warmups_lower_body,
        }
    }
    return render(request, 'entrenador/entrenador.html', context)





@login_required
def workout_detail(request, workout_id):
    if request.user.role != 'ENTRENADOR':
        return redirect('inicio')
    workout = get_object_or_404(Workout, id=workout_id, plan__trainer=request.user)
    exercises = workout.exercises.all().order_by('order')
    context = {
        'workout': workout,
        'exercises': exercises,
    }
    return render(request, 'entrenador/workout_detail.html', context)




@login_required
def create_client(request):
    if request.user.role not in ['ENTRENADOR', 'NUTRICIONISTA']:
        messages.error(request, "No tienes permiso para crear clientes.")
        return redirect('inicio')
    
    if request.method == 'POST':
        form = ClientCreationForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.role = 'CLIENTE'
            client.assigned_professional = request.user

            # Generar una contraseña temporal
            temp_password = get_random_string(length=12)
            client.set_password(temp_password)
            client.save()
            messages.success(request, f"Cliente {client.username} creado exitosamente. Contraseña temporal: {temp_password}")
            return redirect('trainer_dashboard')
        else:
            messages.error(request, "Error al crear el cliente. Revisa los datos ingresados.")
    else:
        form = ClientCreationForm()
    
    return render(request, 'entrenador/crear_cliente.html', {'form': form})













@login_required
def create_plan(request):
    if request.user.role not in ['ENTRENADOR', 'NUTRICIONISTA']:
        messages.error(request, "No tienes permiso para crear planes.")
        return redirect('inicio')
    
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.trainer = request.user
            plan.save()
            messages.success(request, "Plan creado exitosamente.")
            return redirect('trainer_plan_detail', plan_id=plan.id)  
        else:
            messages.error(request, "Error al crear el plan. Revisa los datos ingresados.")
    else:
        form = TrainingPlanForm()
        form.fields['client'].queryset = User.objects.filter(role='CLIENTE', assigned_professional=request.user)
    
    return render(request, 'entrenador/crear_plan.html', {'form': form})












@login_required
def trainer_plan_detail(request, plan_id):
    if request.user.role != 'ENTRENADOR':
        return redirect('inicio')
    plan = get_object_or_404(TrainingPlan, id=plan_id, trainer=request.user)
    workouts = plan.workouts.all().order_by('week_number', 'day_of_week')
    
    total_exercises = WorkoutExercise.objects.filter(workout__plan=plan).count()
    completed_exercises = ExerciseLog.objects.filter(
        workout_exercise__workout__plan=plan, status='completed'
    ).count()
    progress = round((completed_exercises / total_exercises * 100), 2) if total_exercises > 0 else 0
    context = {
        'plan': plan,
        'workouts': workouts,
        'progress': progress,
        'total_exercises': total_exercises,
        'completed_exercises': completed_exercises,
    }
    return render(request, 'entrenador/plan_detail.html', context)




@login_required
def edit_plan(request, plan_id):
    if request.user.role != 'ENTRENADOR':
        return redirect('inicio')
    plan = get_object_or_404(TrainingPlan, id=plan_id, trainer=request.user)
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, "Plan actualizado exitosamente.")
            return redirect('trainer_plan_detail', plan_id=plan.id)
    else:
        form = TrainingPlanForm(instance=plan)
    return render(request, 'entrenador/edit_plan.html', {'form': form, 'plan': plan})




@login_required
def edit_workout_exercise(request, exercise_id):
    if request.user.role != 'ENTRENADOR':
        return redirect('inicio')
    w_exercise = get_object_or_404(WorkoutExercise, id=exercise_id, workout__plan__trainer=request.user)
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST, instance=w_exercise)
        if form.is_valid():
            form.save()
            messages.success(request, "Ejercicio actualizado exitosamente.")
            return redirect('workout_detail', workout_id=w_exercise.workout.id)
    else:
        form = WorkoutExerciseForm(instance=w_exercise)
    return render(request, 'entrenador/edit_ejercicio.html', {'form': form, 'w_exercise': w_exercise})






@login_required
def add_workout(request, plan_id):
    if request.user.role != 'ENTRENADOR':
        return redirect('inicio')
    plan = get_object_or_404(TrainingPlan, id=plan_id, trainer=request.user)
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.plan = plan
            workout.save()
            messages.success(request, "Entrenamiento agregado exitosamente.")
            return redirect('workout_detail', workout_id=workout.id)
    else:
        form = WorkoutForm()
    return render(request, 'entrenador/add_entrenamiento.html', {'form': form, 'plan': plan})



@login_required
def edit_workout(request, workout_id):
    if request.user.role != 'ENTRENADOR':
        return redirect('inicio')
    workout = get_object_or_404(Workout, id=workout_id, plan__trainer=request.user)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrenamiento actualizado exitosamente.")
            return redirect('workout_detail', workout_id=workout.id)
    else:
        form = WorkoutForm(instance=workout)
    return render(request, 'entrenador/edit_workout.html', {'form': form, 'workout': workout})






@login_required
def add_exercise(request, workout_id):
    if request.user.role != 'ENTRENADOR':
        return redirect('inicio')
    workout = get_object_or_404(Workout, id=workout_id, plan__trainer=request.user)
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.workout = workout
            exercise.save()
            messages.success(request, "Ejercicio agregado exitosamente.")
            return redirect('workout_detail', workout_id=workout.id)  # Redirect back to detail to add more
    else:
        form = WorkoutExerciseForm()
    return render(request, 'entrenador/add_ejercicio.html', {'form': form, 'workout': workout})





@login_required
def delete_workout_exercise(request, exercise_id):
    if request.user.role != 'ENTRENADOR':
        return redirect('inicio')
    w_exercise = get_object_or_404(WorkoutExercise, id=exercise_id, workout__plan__trainer=request.user)
    workout_id = w_exercise.workout.id
    w_exercise.delete()
    messages.success(request, "Ejercicio eliminado exitosamente.")
    return redirect('workout_detail', workout_id=workout_id)





@login_required
def update_warmup(request, warmup_id=None):
    if request.user.role != 'ENTRENADOR':
        return redirect('inicio')
    if warmup_id:
        warmup = get_object_or_404(Warmup, id=warmup_id)
    else:
        warmup = None
    if request.method == 'POST':
        form = WarmupForm(request.POST, instance=warmup)
        if form.is_valid():
            form.save()
            return redirect('trainer_dashboard')
    else:
        form = WarmupForm(instance=warmup)
    return render(request, 'entrenador/actualizar_calentamiento.html', {'form': form})




@login_required
def client_dashboard(request):
    if request.user.role != 'CLIENTE':
        return redirect('inicio')
    
    plans = TrainingPlan.objects.filter(client=request.user)
    active_plans_count = plans.filter(status='active').count()
    weekly_sessions = Workout.objects.filter(
        plan__in=plans,
        date__range=[timezone.now().date(), timezone.now().date() + timedelta(days=7)]
    ).exclude(date__isnull=True).count()
    completed_exercises = ExerciseLog.objects.filter(
        client=request.user, status='completed'
    ).count()
    next_session = Workout.objects.filter(
        plan__in=plans,
        date__gte=timezone.now().date()
    ).exclude(date__isnull=True).order_by('date').first()
    upcoming_sessions = Workout.objects.filter(
        plan__in=plans,
        date__gte=timezone.now().date()
    ).exclude(date__isnull=True).order_by('date')[:5]
    total_workouts = Workout.objects.filter(plan__in=plans).count()
    total_exercises = WorkoutExercise.objects.filter(workout__plan__in=plans).count()
    completed_workouts = 0
    for workout in Workout.objects.filter(plan__in=plans):
        workout_exercises_count = workout.exercises.count()
        completed_logs = ExerciseLog.objects.filter(
            workout_exercise__workout=workout,
            status='completed'
        ).count()
        if workout_exercises_count > 0 and completed_logs == workout_exercises_count:
            completed_workouts += 1
    consistency = round((completed_workouts / total_workouts * 100), 2) if total_workouts > 0 else 0
    warmups = Warmup.objects.all()
    warmups_upper_body = warmups.filter(type='superior')
    warmups_lower_body = warmups.filter(type='inferior')
    context = {
        'plans': plans,
        'active_plans_count': active_plans_count,
        'weekly_sessions': weekly_sessions,
        'completed_exercises': completed_exercises,
        'next_session': next_session,
        'upcoming_sessions': upcoming_sessions,
        'total_workouts': total_workouts,
        'total_exercises': total_exercises,
        'consistency': consistency,
        'warmups': {
            'upper_body': warmups_upper_body,
            'lower_body': warmups_lower_body,
        }
    }
    return render(request, 'clientes/cliente.html', context)





@login_required
def client_statistics(request):
    if request.user.role != 'CLIENTE':
        return redirect('inicio')
    logs = ExerciseLog.objects.filter(client=request.user).order_by('-date_completed')
    context = {'logs': logs}
    return render(request, 'clientes/estadisticas.html', context)



@login_required
def view_plan(request, plan_id):
    plan = get_object_or_404(TrainingPlan, id=plan_id, client=request.user)
    workouts = plan.workouts.all().order_by('week_number', 'day_of_week')
    total_exercises = WorkoutExercise.objects.filter(workout__plan=plan).count()
    completed_exercises = ExerciseLog.objects.filter(
        workout_exercise__workout__plan=plan, status='completed'
    ).count()
    progress = round((completed_exercises / total_exercises * 100), 2) if total_exercises > 0 else 0
    completed_workouts = 0
    for workout in workouts:
        workout_exercises = workout.exercises.count()
        completed_workout_exercises = ExerciseLog.objects.filter(
            workout_exercise__workout=workout, status='completed'
        ).count()
        if workout_exercises > 0 and completed_workout_exercises == workout_exercises:
            completed_workouts += 1
    context = {
        'plan': plan,
        'workouts': workouts,
        'progress': progress,
        'total_exercises': total_exercises,
        'completed_exercises': completed_exercises,
        'completed_workouts': completed_workouts,
    }
    return render(request, 'clientes/ver_plan.html', context)



@login_required
def log_exercise(request, workout_exercise_id):
    workout_exercise = get_object_or_404(WorkoutExercise, id=workout_exercise_id, workout__plan__client=request.user)
    best_log = ExerciseLog.objects.filter(
        client=request.user,
        workout_exercise__exercise=workout_exercise.exercise
    ).order_by('-weight_lifted_kg', '-reps_completed').first()
    if request.method == 'POST':
        form = ExerciseLogForm(request.POST, request.FILES)
        if form.is_valid():
            log = form.save(commit=False)
            log.client = request.user
            log.workout_exercise = workout_exercise
            log.save()
            trainer_email = workout_exercise.workout.plan.trainer.email
            subject = f"Reporte de Entrenamiento de {request.user.username}"
            message = f"""
            El cliente {request.user.username} ha completado el ejercicio {workout_exercise.exercise.name}.
            
            Detalles:
            - Peso: {log.weight_lifted_kg} kg
            - Repeticiones: {log.reps_completed}
            - RIR: {log.rir_actual}
            - RPE: {log.rpe_actual}
            - Estado: {log.get_status_display()}
            - Notas: {log.notes}
            
            Fecha: {log.date_completed.strftime('%d/%m/%Y')}
            """
            send_mail(subject, message, settings.EMAIL_HOST_USER, [trainer_email])
            return redirect('view_plan', plan_id=workout_exercise.workout.plan.id)
    else:
        form = ExerciseLogForm()
    context = {
        'form': form,
        'workout_exercise': workout_exercise,
        'best_log': best_log,
    }
    return render(request, 'clientes/report.html', context)




@login_required
def view_log(request, log_id):
    log = get_object_or_404(ExerciseLog, id=log_id)
    if request.user.role == 'ENTRENADOR' and log.workout_exercise.workout.plan.trainer == request.user:
        pass
    elif request.user.role == 'CLIENTE' and log.client == request.user:
        pass
    else:
        messages.error(request, "No tienes permiso para ver este registro.")
        return redirect('inicio')
    context = {'log': log}
    return render(request, 'entrenamiento/view_log.html', context)




@login_required
def nutritionist_dashboard(request):
    if request.user.role != 'NUTRICIONISTA':
        return redirect('inicio')
    # Implement as needed
    return render(request, 'nutricionistas/nutricionistas.html')