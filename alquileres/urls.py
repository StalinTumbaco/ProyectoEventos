from django.urls import path
from . import views

urlpatterns = [
    path('alquilar/<int:evento_id>/', views.alquilar_evento, name='alquilar_evento'),
    path('cancelar/<int:alquiler_id>/', views.cancelar_alquiler, name='cancelar_alquiler'),
]
