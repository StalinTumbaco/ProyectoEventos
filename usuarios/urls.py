from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('verificar-codigo/<str:username>/', views.verificar_codigo, name='verificar_codigo'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
]