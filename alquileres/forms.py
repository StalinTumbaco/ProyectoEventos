from django.forms import ModelForm
from .models import * 

class FormAlquiler(ModelForm):
    class Meta:
        model = Alquiler
        fields = ['fecha_alquiler','horainicio_planificada_reserva',
                  'horafin_planificada_reserva','horafin_real_reserva','costo_alquiler'
                  ,'calificacion_negocio','observacion','cantidad_anticipo ','estado_alquiler']

class FormFoto(ModelForm):
    class Meta:
        model = FotoAlquiler
        fields = [
            'imagen','descripcion ','fecha_subida'
            'likes','dislikes'
        ]

class FormAlquilerServicio(ModelForm):
    class Meta:
        model = AlquilerServicio
        fields = [
            'cantidad','costo_total','calificacion_cliente'
        ]