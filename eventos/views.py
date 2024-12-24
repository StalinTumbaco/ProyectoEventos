from django.shortcuts import render
from .models import Evento, TipoDeEvento

# Create your views here.
def home (request):
    return render(request, 'home.html')

def eventos (request):
    events = Evento.objects.all()
    tipevents = TipoDeEvento.objects.all()
    return render(request, 'eventos.html', {'tipo_eventos': tipevents, 'eventos': events})