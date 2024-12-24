from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField

class Alquiler(models.Model):
    idalquiler = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evento = models.ForeignKey('eventos.Evento', on_delete=models.CASCADE)
    fecha_alquiler = models.DateField()
    horainicio_planificada_reserva = models.TimeField()
    horafin_planificada_reserva = models.TimeField()
    horafin_real_reserva = models.TimeField(blank=True, null=True)
    costo_alquiler = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    calificacion_negocio = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    observacion = models.TextField(blank=True, null=True)
    cantidad_anticipo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0.01)])
    estados = [('pendiente', 'Pendiente'), ('cancelado', 'Cancelado'), ('completado', 'Completado'),]
    estado_alquiler = models.CharField(max_length=30, choices=estados)

    def clean(self):
        # Validar que la hora final no sea anterior a la hora inicial
        if self.horafin_planificada_reserva and self.horafin_planificada_reserva < self.horainicio_planificada_reserva:
            raise ValidationError({
                'horafin_planificada_reserva': _('La hora final planificada no puede ser anterior a la hora inicial.')
            })
        if self.calificacion_negocio and (self.calificacion_negocio < 1 or self.calificacion_negocio > 5):
            raise ValidationError({'calificacion_negocio': 'La calificación debe estar entre 1 y 5.'})

    def __str__(self):
        return f"Alquiler #{self.idalquiler} - Cliente: {self.cliente.username}"


class FotoAlquiler(models.Model):
    idfoto_alquiler = models.AutoField(primary_key=True)
    evento = models.ForeignKey('eventos.Evento', on_delete=models.CASCADE)
    imagen = CloudinaryField('image', null=True, blank=True, default=None)
    descripcion = models.CharField(max_length=200)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    alquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        return f"Foto {self.idfoto_alquiler} del Evento {self.evento}"


class AlquilerServicio(models.Model):
    idalquiler_servicio = models.AutoField(primary_key=True)
    alquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE)
    servicio = models.ForeignKey('servicios.Servicio', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    calificacion_cliente = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    def save(self, *args, **kwargs):
        # Calcular costo_total antes de guardar
        if self.servicio and self.cantidad:
            self.costo_total = self.cantidad * self.servicio.valor_unidad
        super().save(*args, **kwargs)  # Llama al método original `save()`

    def __str__(self):
        return f"Servicio #{self.idalquiler_servicio} - Alquiler #{self.alquiler.idalquiler}"
