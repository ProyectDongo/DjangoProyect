from django.urls import path

from .views import (
    trainer_dashboard, create_plan, add_workout, add_exercise, client_dashboard,
    view_plan, log_exercise, update_warmup, create_client, trainer_plan_detail,
    workout_detail, edit_plan, edit_workout, edit_workout_exercise, delete_workout_exercise,
    client_statistics, view_log,client_logs,create_exercise,progress_view,
    generate_presigned_url,initiate_multipart_upload,generate_presigned_part,complete_multipart_upload,delete_workout,delete_plan,delete_workout

)

urlpatterns = [
    # Trainer Dashboard and Client Management
    path('crear-cliente/', create_client, name='create_client'),
    path('trainer/', trainer_dashboard, name='trainer_dashboard'),
    path('client_statistics/', client_statistics, name='client_statistics'),

    # Client Dashboard and Views
    path('client/', client_dashboard, name='client_dashboard'),
    path('view_plan/<int:plan_id>/', view_plan, name='view_plan'),
    path('client/<int:client_id>/logs/', client_logs, name='client_logs'),

    # Training Plan Management
    path('create_plan/', create_plan, name='create_plan'),
    path('plan/<int:plan_id>/', trainer_plan_detail, name='plan_detail'),
    path('trainer_plan/<int:plan_id>/', trainer_plan_detail, name='trainer_plan_detail'),
    path('edit_plan/<int:plan_id>/', edit_plan, name='edit_plan'),
    path('entrenamiento/delete_plan/<int:plan_id>/', delete_plan, name='delete_plan'),

    # Workout Management
    path('add_workout/<int:plan_id>/', add_workout, name='add_workout'),
    path('workout/<int:workout_id>/', workout_detail, name='workout_detail'),
    path('edit_workout/<int:workout_id>/', edit_workout, name='edit_workout'),
    path('entrenamiento/delete_workout/<int:workout_id>/', delete_workout, name='delete_workout'),

    # Exercise Management
    path('add_exercise/<int:workout_id>/', add_exercise, name='add_exercise'),
    path('create_exercise/', create_exercise, name='create_exercise'),
    path('edit_workout_exercise/<int:exercise_id>/', edit_workout_exercise, name='edit_workout_exercise'),
    path('delete_workout_exercise/<int:exercise_id>/', delete_workout_exercise, name='delete_workout_exercise'),

    # Logs and Progress
    path('view_log/<int:log_id>/', view_log, name='view_log'),
    path('progress/<int:plan_id>/', progress_view, name='progress_view'),
    path('log_exercise/<int:workout_exercise_id>/', log_exercise, name='log_exercise'),

    # Warmup Management
    path('update_warmup/', update_warmup, name='create_warmup'),
    path('update_warmup/<int:warmup_id>/', update_warmup, name='update_warmup'),
    path('warmup/update/', update_warmup, name='create_warmup'),
    path('warmup/update/<int:warmup_id>/', update_warmup, name='update_warmup'),

    # File Upload Management
    path('generate-presigned/', generate_presigned_url, name='generate_presigned'),
    path('initiate_multipart/', initiate_multipart_upload, name='initiate_multipart_upload'),
    path('generate_presigned_part/', generate_presigned_part, name='generate_presigned_part'),
    path('complete_multipart/', complete_multipart_upload, name='complete_multipart_upload'),
]