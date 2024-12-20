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
            'nacionalidad',      # Nacionalidad (país)
            'genero',            # Género
        ]

        widgets = {
            'genero': forms.Select(choices=[
                ('Masculino', 'Masculino'),
                ('Femenino', 'Femenino'),
                ('No binario', 'No binario'),
            ]),
        }
