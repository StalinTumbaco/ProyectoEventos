from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class UsuarioEmailBackend(ModelBackend):
    """
    Permite autenticar usuarios con nombre de usuario o correo electrónico.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Busca al usuario por nombre de usuario o correo electrónico
            usuario = Usuario.objects.get(
                username=username
            ) if Usuario.objects.filter(username=username).exists() else Usuario.objects.get(email=username)
        except Usuario.DoesNotExist:
            return None

        if usuario.check_password(password) and self.user_can_authenticate(usuario):
            return usuario

        return None
