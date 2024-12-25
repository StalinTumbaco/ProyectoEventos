from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Evento, TipoDeEvento

# Create your views here.
def home (request):
    return render(request, 'home.html')

def eventos (request):
    events = Evento.objects.all()
    tipevents = TipoDeEvento.objects.all()
    return render(request, 'eventos.html', {'tipo_eventos': tipevents, 'eventos': events})

def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    return render(request, 'detalle_evento.html', {'evento': evento})