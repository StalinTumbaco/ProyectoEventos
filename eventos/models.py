from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

class TipoDeEvento(models.Model):
    idtipo_de_evento = models.AutoField(primary_key=True)
    nombre_evento = models.CharField(max_length=50)
    imagen = CloudinaryField('image', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_evento


class Evento(models.Model):
    idevento = models.AutoField(primary_key=True)
    titulo_evento = models.CharField(max_length=50, null=False, blank=False, default="Sin título")
    descripcion = models.TextField()
    valor_referencial = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    numero_horas_permitidas = models.PositiveIntegerField()
    valor_extra_hora = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tipo_de_evento = models.ForeignKey(TipoDeEvento, on_delete=models.CASCADE, related_name="eventos")

    def clean(self):
        super().clean()
        if self.valor_referencial < 0:
            raise ValidationError({
                'valor_referencial': _('El valor referencial no puede ser negativo.'),
                'valor_extra_hora' : _('El valor de la hora extra no puede ser negativo.'),
            })

    def __str__(self):
        return f"Evento #{self.idevento} - {self.titulo_evento}..."


class Promocion(models.Model):
    idpromocion = models.AutoField(primary_key=True)
    descripcion_promocion = models.CharField(max_length=100)
    valor_referencial_promo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tipo_promocion = models.CharField(max_length=100)
    porcentaje_promocion = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    fecha_vigencia = models.DateField()
    fecha_caducidad = models.DateField()
    estado_promocion = models.CharField(max_length=20, choices=[('vigente', 'Vigente'), ('caducado', 'Caducado'), ('n/a', 'N/A')])
    tipo_de_evento = models.ForeignKey(TipoDeEvento, on_delete=models.CASCADE, related_name="promocion", null=True, blank=True)

    def clean(self):
        super().clean()
        if self.fecha_vigencia > self.fecha_caducidad:
            raise ValidationError({
                'fecha_vigencia': _('La fecha de vigencia no puede ser mayor a la fecha de caducidad.')
            })

    def __str__(self):
        return f"Promoción #{self.idpromocion} - {self.descripcion_promocion}"


class Eventualidad(models.Model):
    ideventualidad = models.AutoField(primary_key=True)
    tipo_eventualidad = models.CharField(max_length=20, null=False, blank=False, default="General")
    descripcion_eventualidad = models.CharField(max_length=200)
    fecha_eventualidad = models.DateField()
    costo_eventualidad = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    responsable = models.CharField(max_length=100)
    fecha_resolucion = models.DateField(blank=True, null=True)
    eventualidad_servicio = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="eventualidad", null=True, blank=True)

    def __str__(self):
        return f"Eventualidad #{self.ideventualidad} - {self.descripcion_eventualidad[:50]}..."
