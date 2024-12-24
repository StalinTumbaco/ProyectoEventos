from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.

class Servicio(models.Model):
    idservicio = models.AutoField(primary_key=True)
    Nombre_servicio = models.CharField(max_length=50, null=False, blank=False, default="Sin título")
    descripcion_servicio = models.CharField(max_length=150, null = False, blank=False, default=False)
    valor_unidad = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estados =[('disponible', 'Disponible'), ('ocupado','Ocupado'), ('cancelado','Cancelado'),]
    estado_servicio = models.CharField(max_length=100, choices=estados)
    fecha_emision = models.DateTimeField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    descripcion_unidad = models.TextField(max_length=200, blank=False, null=False, default=False)
    fecha_actualizacion_precio = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        # Validar que fecha_entrega no sea anterior a fecha_emision
        if self.fecha_entrega and self.fecha_entrega < self.fecha_emision:
            raise ValidationError({
                'fecha_entrega': _ ('La fecha de entrega no puede ser anterior a la fecha de emisión.')
            })
        if self.valor_unidad < 0:
            raise ValidationError({
                'valor_unidad': _('El valor de la unidad no puede ser inferior a 0,01 ctvs.')
            })

    def __str__(self):
        return self.descripcion_servicio


class FotoServicio(models.Model):
    idfoto_servicio = models.AutoField(primary_key=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    imagen = CloudinaryField('image', null=True)
    descripcion_foto = models.TextField(max_length=200, null=False, blank=False, default=False)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Foto {self.idfoto_servicio} del Servicio {self.servicio.descripcion_servicio}"
