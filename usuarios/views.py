from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth import authenticate, login
from usuarios.forms import RegistroForm
from django.contrib import messages

# Create your views here.
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # Guarda los datos del formulario sin enviar a la base de datos
            usuario.fecha_registro = now()  # Agrega la fecha de registro
            usuario.save()  # Guarda el usuario en la base de datos
            login (request, usuario)
            return redirect('login')  # Redirige al login (ajusta según tu proyecto)
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username_email = request.POST.get('username_email')
        password = request.POST.get('password')

        # Autentica al usuario con nombre de usuario o correo
        usuario = authenticate(request, username=username_email, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect('home')  # Cambia 'home' a la URL que corresponda
        else:
            messages.error(request, 'Nombre de usuario, correo o contraseña incorrectos.')

    return render(request, 'login.html')