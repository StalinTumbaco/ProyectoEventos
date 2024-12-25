from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la página de inicio de la app eventos
    path('eventos/', views.eventos, name='eventos'),
    path('evento/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)