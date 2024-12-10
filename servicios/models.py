from django.db import models

# Create your models here.

class Servicio(models.Model):
    idservicio = models.AutoField(primary_key=True)
    descripcion_servicio = models.CharField(max_length=150)
    valor_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    estado_servicio = models.CharField(max_length=100)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    descripcion_unidad = models.CharField(max_length=200, blank=True, null=True)
    fecha_actualizacion_precio = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descripcion_servicio


class FotoServicio(models.Model):
    idfoto_servicio = models.AutoField(primary_key=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    url_imagen = models.URLField(max_length=255)
    descripcion_foto = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f"Foto {self.idfoto_servicio} del Servicio {self.servicio.descripcion_servicio}"
