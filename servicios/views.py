from django.shortcuts import render
from .models import Servicio
# Create your views here.

def servicios (request):
    services = Servicio.objects.all()
    return render(request, 'services.html', {'servicios': services})