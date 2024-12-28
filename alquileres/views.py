from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Alquiler, AlquilerServicio
from eventos.models import Evento
from servicios.models import Servicio
from .forms import AlquilerForm, AlquilerServicioForm

#Create your views here.

@login_required
def alquilar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)

    if request.method == 'POST':
        form = AlquilerForm(request.POST)
        if form.is_valid():
            alquiler = form.save(commit=False)
            alquiler.cliente = request.user
            alquiler.evento = evento
            alquiler.estado_alquiler = 'pendiente'

            # Calcular el costo del alquiler
            horainicio = form.cleaned_data['horainicio_planificada_reserva']
            horafin = form.cleaned_data['horafin_planificada_reserva']
            fecha_base = datetime.combine(alquiler.fecha_alquiler, datetime.min.time())

            # Convertir las horas a datetime
            datetime_inicio = datetime.combine(fecha_base.date(), horainicio)
            datetime_fin = datetime.combine(fecha_base.date(), horafin)

            # Calcular la diferencia en horas
            diferencia_horas = Decimal ((datetime_fin - datetime_inicio).total_seconds() / 3600)
            alquiler.costo_alquiler = diferencia_horas * evento.valor_referencial

            alquiler.save()
            return redirect('perfil_usuario')  # Redirige al perfil del usuario
    else:
        form = AlquilerForm()

    return render(request, 'alquilar_evento.html', {'form': form, 'evento': evento})

@login_required
def cancelar_alquiler(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, pk=alquiler_id, cliente=request.user)
    alquiler.delete()
    return redirect('perfil_usuario')

@login_required
def alquilar_servicio(request, idservicio):
    servicio = get_object_or_404(Servicio, idservicio=idservicio)
    if request.method == 'POST':
        form = AlquilerServicioForm(request.POST)
        if form.is_valid():
            alquiler_servicio = form.save(commit=False)
            alquiler_servicio.alquiler.cliente = request.user
            alquiler_servicio.save()
            return redirect('perfil_usuario')
    else:
        form = AlquilerServicioForm()
    return render(request, 'alquilar_servicio.html', {'form': form, 'servicio': servicio})

@login_required
def cancelar_alquiler_servicio(request, idalquiler_servicio):
    alquiler_servicio = get_object_or_404(AlquilerServicio, pk=idalquiler_servicio, cliente=request.user)
    alquiler_servicio.delete()
    return redirect('perfil_usuario')