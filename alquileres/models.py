from django.db import models
from django.contrib.auth.models import User  # Para usar el modelo User de Django
from django.conf import settings

class Alquiler(models.Model):
    idalquiler = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evento = models.ForeignKey('eventos.Evento', on_delete=models.CASCADE)
    fecha_alquiler = models.DateField()
    horainicio_planificada_reserva = models.TimeField()
    horafin_planificada_reserva = models.TimeField()
    horafin_real_reserva = models.TimeField(blank=True, null=True)
    costo_alquiler = models.DecimalField(max_digits=10, decimal_places=2)
    calificacion_negocio = models.IntegerField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    cantidad_anticipo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado_alquiler = models.CharField(max_length=30)

    def __str__(self):
        return f"Alquiler #{self.idalquiler} - Cliente: {self.cliente.username}"


class FotoAlquiler(models.Model):
    idfoto_alquiler = models.AutoField(primary_key=True)
    evento = models.ForeignKey('eventos.Evento', on_delete=models.CASCADE)
    url_foto = models.URLField(max_length=255)
    descripcion = models.CharField(max_length=200)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f"Foto {self.idfoto_alquiler} del Evento {self.evento}"


class AlquilerServicio(models.Model):
    idalquiler_servicio = models.AutoField(primary_key=True)
    alquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE)
    servicio = models.ForeignKey('servicios.Servicio', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)
    calificacion_cliente = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Servicio #{self.idalquiler_servicio} - Alquiler #{self.alquiler.idalquiler}"
