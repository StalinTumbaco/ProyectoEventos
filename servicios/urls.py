from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.servicios, name='servicios'),
    path('services/<int:servicio_id>/', views.detalle_servicio, name='detalle_servicio'),
]