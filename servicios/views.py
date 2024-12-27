from django.shortcuts import render, get_object_or_404
from .models import Servicio, FotoServicio
# Create your views here.

def servicios (request):
    services = Servicio.objects.prefetch_related('fotoservicio_set').all()
    return render(request, 'services.html', {'servicios': services})

def detalle_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    fotos = Servicio.objects.prefetch_related('fotoservicio_set').all()
    return render(request, 'detalle_servicio.html', {'servicio': servicio, 'fotos': fotos})