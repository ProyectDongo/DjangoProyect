from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ExerciseForm  # Asegúrate de que ExerciseForm esté importado correctamente

@login_required
def create_exercise(request):
    if request.user.role != 'ENTRENADOR':
        messages.error(request, "No tienes permiso para crear ejercicios.")
        return redirect('inicio')
    
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ejercicio creado exitosamente.")
            return redirect('trainer_dashboard')
        else:
            messages.error(request, "Error al crear el ejercicio. Revisa los datos ingresados.")
    else:
        form = ExerciseForm()
    
    return render(request, 'entrenador/create_exercise.html', {'form': form})