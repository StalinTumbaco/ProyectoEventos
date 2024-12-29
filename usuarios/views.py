from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.core.cache import cache
from .forms import RegistroForm
from .models import Usuario
from django.contrib import messages

# Create your views here.
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Crear un diccionario con los datos del usuario sin guardarlo en la base de datos
            user_data = {
                'username': form.cleaned_data['username'],
                'first_name':form.cleaned_data['first_name'],
                'last_name':form.cleaned_data['last_name'],
                'identificacion_cliente':form.cleaned_data['identificacion_cliente'],
                'telefono':form.cleaned_data['telefono'],
                'email': form.cleaned_data['email'],
                'nacionalidad': form.cleaned_data['nacionalidad'],
                'genero': form.cleaned_data['genero'],
                'password': form.cleaned_data['password1'],  # Usar password1 para obtener la contraseña
                'fecha_registro': now(),
            }
            
            # Generar un código único de verificación
            verification_code = get_random_string(length=6, allowed_chars='0123456789')
            cache.set(f'registration_data_{user_data["username"]}', user_data, timeout=600)  # Guardar datos por 10 minutos
            cache.set(f'verification_code_{user_data["username"]}', verification_code, timeout=600)  # Guardar código por 10 minutos
            
            # Enviar el código al correo electrónico
            send_mail(
                'Código de Verificación',
                f'Tu código de verificación es: {verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [user_data['email']],
                fail_silently=False,
            )
            
            # Redirigir a la página de verificación
            return redirect('verificar_codigo', username=user_data['username'])
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


def verificar_codigo(request, username):
    if request.method == 'POST':
        input_code = request.POST.get('codigo')
        saved_code = cache.get(f'verification_code_{username}')
        user_data = cache.get(f'registration_data_{username}')
        
        if saved_code and input_code == saved_code and user_data:
            # Crear el usuario y guardarlo en la base de datos
            user = Usuario.objects.create_user(
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                identificacion_cliente=user_data['identificacion_cliente'],
                telefono=user_data['telefono'],
                email=user_data['email'],
                nacionalidad=user_data['nacionalidad'],
                genero=user_data['genero'],
                password=user_data['password'],
            )
            user.fecha_registro = user_data['fecha_registro']
            user.is_active = True
            user.save()
            
            # Iniciar sesión y redirigir al home
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Limpiar datos de la caché
            cache.delete(f'verification_code_{username}')
            cache.delete(f'registration_data_{username}')
            return redirect('home')
        else:
            return render(request, 'verificar_codigo.html', {'error': 'Código inválido o expirado.'})
    
    return render(request, 'verificar_codigo.html')


def login_view(request):
    if request.method == 'POST':
        username_email = request.POST.get('username_email')
        password = request.POST.get('password')

        # Autentica al usuario con nombre de usuario o correo
        usuario = authenticate(request, username=username_email, password=password)

        if usuario is not None:
            login(request, usuario)
            if usuario.is_superuser or usuario.is_staff:
                return redirect('/admin/')
            return redirect('home')  # Cambia 'home' a la URL que corresponda
        else:
            messages.error(request, 'Nombre de usuario, correo o contraseña incorrectos.')

    return render(request, 'login.html')

def cerrar_sesion (request):
    logout(request)
    return redirect ('home')

@login_required
def profile_user(request):
    return render (request, "perfil.html", {"Usuario": request.user})

@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        usuario = request.user
        usuario.username = request.POST.get('username', usuario.username)
        usuario.first_name = request.POST.get('first_name', usuario.first_name)
        usuario.last_name = request.POST.get('last_name', usuario.last_name)
        usuario.nacionalidad = request.POST.get('nacionalidad', usuario.nacionalidad)
        usuario.telefono = request.POST.get('telefono', usuario.telefono)
        usuario.save()
        messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
        return redirect('perfil_usuario')  # Redirige a la página del perfil
    return redirect('perfil_usuario')  # Evita accesos no permitidos

def recuperar_contrasena(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Usuario.objects.get(email=email)
            verification_code = get_random_string(length=6, allowed_chars='0123456789')
            
            # Guardar el código en caché con un tiempo de expiración
            cache.set(f'password_reset_code_{user.username}', verification_code, timeout=600)  # 10 minutos

            # Enviar el código por correo
            send_mail(
                'Recuperación de Contraseña',
                f'Tu código de verificación para recuperar tu contraseña es: {verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return redirect('verificar_codigo_reset', username=user.username)
        except Usuario.DoesNotExist:
            messages.error(request, 'El correo electrónico ingresado no está registrado.')
    
    return render(request, 'recuperar_contrasena.html')

def verificar_codigo_reset(request, username):
    if request.method == 'POST':
        input_code = request.POST.get('codigo')
        saved_code = cache.get(f'password_reset_code_{username}')
        
        if saved_code and input_code == saved_code:
            return redirect('resetear_contrasena', username=username)
        else:
            messages.error(request, 'Código inválido o expirado.')
    
    return render(request, 'verificar_codigo_reset.html')

def resetear_contrasena(request, username):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            try:
                user = Usuario.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                
                # Eliminar el código de caché
                cache.delete(f'password_reset_code_{username}')
                
                messages.success(request, 'Tu contraseña ha sido actualizada. Ahora puedes iniciar sesión.')
                return redirect('login')
            except Usuario.DoesNotExist:
                messages.error(request, 'Ocurrió un error al actualizar la contraseña.')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
    
    return render(request, 'resetear_contrasena.html')