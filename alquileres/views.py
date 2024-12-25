from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Alquiler
from eventos.models import Evento

#Create your views here.

@login_required
def alquilar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    # Verifica si ya está alquilado por el usuario
    if Alquiler.objects.filter(cliente=request.user, evento=evento, estado_alquiler='pendiente').exists():
        # Redirigir con un mensaje si ya está alquilado
        return redirect('detalle_evento', evento_id=evento_id)

    # Crear un nuevo alquiler
    Alquiler.objects.create(
        cliente=request.user,
        evento=evento,
        fecha_alquiler=now().date(),
        horainicio_planificada_reserva=now().time(),
        horafin_planificada_reserva=now().time(),  # Cambia según tu lógica
        costo_alquiler=evento.valor_referencial,  # Cambia según el costo real
        estado_alquiler='pendiente',
    )

    return redirect('perfil_usuario')

@login_required
def cancelar_alquiler(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, pk=alquiler_id, cliente=request.user)
    alquiler.delete()
    return redirect('perfil_usuario')
