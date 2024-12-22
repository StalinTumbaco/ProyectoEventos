from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Campos adicionales que no están en el modelo User por defecto
    identificacion_cliente = models.CharField(max_length=20)
    nacionalidad = models.CharField(max_length=100)
    fecha_registro = models.DateField(auto_now_add=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    genero = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.identificacion_cliente}"
