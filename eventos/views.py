from django.shortcuts import render
from .models import Evento

# Create your views here.
def home (request):
    return render(request, 'home.html')

def eventos (request):
    events = Evento.objects.all()
    return render(request, 'eventos.html', {'eventos': events})