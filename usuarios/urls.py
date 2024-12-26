from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('verificar-codigo/<str:username>/', views.verificar_codigo, name='verificar_codigo'),
    path('login/', views.login_view, name='login'),
    path('perfil/', views.profile_user, name='perfil_usuario'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('actualizar_perfil/', views.actualizar_perfil, name='actualizar_perfil'),
]