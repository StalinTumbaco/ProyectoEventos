from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.servicios, name='servicios')
]