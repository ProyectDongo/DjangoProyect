from django.urls import path

from .views import (
    trainer_dashboard, create_plan, add_workout, add_exercise, client_dashboard,
    view_plan, log_exercise, update_warmup, create_client, trainer_plan_detail,
    workout_detail, edit_plan, edit_workout, edit_workout_exercise, delete_workout_exercise,
    client_statistics, view_log,client_logs,create_exercise
)

urlpatterns = [
    path('crear-cliente/', create_client, name='create_client'),
    path('trainer/', trainer_dashboard, name='trainer_dashboard'),
    path('create_plan/', create_plan, name='create_plan'),
    path('add_workout/<int:plan_id>/', add_workout, name='add_workout'),
    path('add_exercise/<int:workout_id>/', add_exercise, name='add_exercise'),
    path('client/', client_dashboard, name='client_dashboard'),
    path('view_plan/<int:plan_id>/', view_plan, name='view_plan'),
    path('log_exercise/<int:workout_exercise_id>/', log_exercise, name='log_exercise'),
    path('update_warmup/', update_warmup, name='create_warmup'),
    path('update_warmup/<int:warmup_id>/', update_warmup, name='update_warmup'),
    path('plan/<int:plan_id>/', trainer_plan_detail, name='plan_detail'),
    path('workout/<int:workout_id>/', workout_detail, name='workout_detail'),
    path('trainer_plan/<int:plan_id>/', trainer_plan_detail, name='trainer_plan_detail'),
    path('warmup/update/', update_warmup, name='create_warmup'),
    path('warmup/update/<int:warmup_id>/', update_warmup, name='update_warmup'),
    path('edit_plan/<int:plan_id>/', edit_plan, name='edit_plan'),
    path('edit_workout/<int:workout_id>/', edit_workout, name='edit_workout'),
    path('edit_workout_exercise/<int:exercise_id>/', edit_workout_exercise, name='edit_workout_exercise'),
    path('delete_workout_exercise/<int:exercise_id>/', delete_workout_exercise, name='delete_workout_exercise'),
    path('client_statistics/', client_statistics, name='client_statistics'),
    path('view_log/<int:log_id>/', view_log, name='view_log'),
    path('client/<int:client_id>/logs/', client_logs, name='client_logs'),
    path('create_exercise/', create_exercise, name='create_exercise'),
]