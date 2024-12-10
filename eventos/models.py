from django.db import models

class TipoDeEvento(models.Model):
    idtipo_de_evento = models.AutoField(primary_key=True)
    nombre_evento = models.CharField(max_length=50)
    url_imagen = models.URLField(max_length=200, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_evento


class Evento(models.Model):
    idevento = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    valor_referencial = models.DecimalField(max_digits=10, decimal_places=2)
    numero_horas_permitidas = models.IntegerField()
    valor_extra_hora = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_de_evento = models.ForeignKey(TipoDeEvento, on_delete=models.CASCADE, related_name="eventos")

    def __str__(self):
        return f"Evento #{self.idevento} - {self.descripcion[:50]}..."


class Promocion(models.Model):
    idpromocion = models.AutoField(primary_key=True)
    descripcion_promocion = models.CharField(max_length=100)
    valor_referencial_promo = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_promocion = models.CharField(max_length=100)
    porcentaje_promocion = models.IntegerField()
    fecha_vigencia = models.DateField()
    fecha_caducidad = models.DateField()
    estado_promocion = models.CharField(max_length=20)

    def __str__(self):
        return f"Promoción #{self.idpromocion} - {self.descripcion_promocion}"


class Eventualidad(models.Model):
    ideventualidad = models.AutoField(primary_key=True)
    descripcion_eventualidad = models.CharField(max_length=200)
    fecha_eventualidad = models.DateField()
    tipo_eventualidad = models.CharField(max_length=20)
    costo_eventualidad = models.DecimalField(max_digits=10, decimal_places=2)
    responsable = models.CharField(max_length=100)
    fecha_resolucion = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Eventualidad #{self.ideventualidad} - {self.descripcion_eventualidad[:50]}..."
