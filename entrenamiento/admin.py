from django.contrib import admin

from .models import TrainingPlan, Workout, WorkoutExercise,ExerciseLog


class trainingPlanAdmin(admin.ModelAdmin):
    pass 


class workoutAdmin(admin.ModelAdmin):
    pass

class workoutExerciseAdmin(admin.ModelAdmin):
    pass


class exerciseLogAdmin(admin.ModelAdmin):
    pass



admin.site.register(TrainingPlan, trainingPlanAdmin)
admin.site.register(Workout, workoutAdmin)
admin.site.register(WorkoutExercise, workoutExerciseAdmin)
admin.site.register(ExerciseLog, exerciseLogAdmin)
admin.site.site_header = "Administración de FitnessPro"
admin.site.site_title = "FitnessPro Admin"  