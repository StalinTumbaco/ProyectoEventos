from django.shortcuts import render, redirect
from django.utils.timezone import now
from usuarios.forms import RegistroForm

# Create your views here.
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # Guarda los datos del formulario sin enviar a la base de datos
            usuario.fecha_registro = now()  # Agrega la fecha de registro
            usuario.save()  # Guarda el usuario en la base de datos
            return redirect('login')  # Redirige al login (ajusta según tu proyecto)
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})
