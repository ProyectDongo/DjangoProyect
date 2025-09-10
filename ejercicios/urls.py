# entrenamiento/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create_exercise/', views.create_exercise, name='create_exercise'),
]