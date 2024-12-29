from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import Usuario

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'username',          # Nombre de usuario
            'first_name',        # Nombre
            'last_name',         # Apellido
            'identificacion_cliente',  # Identificación
            'telefono',          # Teléfono
            'email',             #correoelectronico
            'nacionalidad',      # Nacionalidad (país)
            'genero',            # Género
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'identificacion_cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Identificación'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nacionalidad'}),
            'genero': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('Masculino', 'Masculino'),
                ('Femenino', 'Femenino'),
                ('No binario', 'No binario'),
            ]),
        }
