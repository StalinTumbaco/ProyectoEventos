from django.forms import ModelForm, DateField, DateInput, TimeField, TimeInput, NumberInput
from .models import * 
from datetime import date, time

class AlquilerForm(ModelForm):
    class Meta:
        model = Alquiler
        fields = ['fecha_alquiler', 'horainicio_planificada_reserva', 'horafin_planificada_reserva']

    fecha_alquiler = DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de Alquiler"
    )
    horainicio_planificada_reserva = TimeField(
        widget=TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label="Hora de Inicio"
    )
    horafin_planificada_reserva = TimeField(
        widget=TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label="Hora de Fin"
    )

    def clean(self):
        cleaned_data = super().clean()
        fecha_alquiler = cleaned_data.get('fecha_alquiler')
        horainicio = cleaned_data.get('horainicio_planificada_reserva')
        horafin = cleaned_data.get('horafin_planificada_reserva')

        # Validar que la hora de inicio sea antes de la hora final
        if horainicio and horafin and horainicio >= horafin:
            self.add_error('horainicio_planificada_reserva', "La hora de inicio debe ser anterior a la hora de fin.")
            self.add_error('horafin_planificada_reserva', "La hora de fin debe ser posterior a la hora de inicio.")

        # Validar que no haya conflictos con reservas existentes
        if fecha_alquiler and horainicio and horafin:
            reservas = Alquiler.objects.filter(
                fecha_alquiler=fecha_alquiler,
                estado_alquiler='pendiente'
            )
            for reserva in reservas:
                if (horainicio < reserva.horafin_planificada_reserva and horafin > reserva.horainicio_planificada_reserva):
                    raise ValidationError(
                        f"El rango de horas {horainicio} - {horafin} está ocupado. Selecciona otro rango."
                    )

        return cleaned_data

class AlquilerServicioForm(ModelForm):
    class Meta:
        model = AlquilerServicio
        fields = ['alquiler','servicio', 'cantidad']
        widgets = {
            'cantidad': NumberInput(attrs={'min': 1}),
        }