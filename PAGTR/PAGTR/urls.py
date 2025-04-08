"""PAGTR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django import views
from PAGTR.TransporteAPP import views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='/index/')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('ruta/<int:ruta_id>/', views.detalle_ruta, name='detalle_ruta'),
    path('perfil/<int:usuario_id>/', views.perfil_usuario, name='perfil_usuario'),
    path('ruta/editar/<int:ruta_id>/', views.editar_ruta, name='editar_ruta'),
    path('ruta/eliminar/<int:ruta_id>/', views.eliminar_ruta, name='eliminar_ruta'),
    path('crear_residencia/', views.crear_residencia, name="crear_residencia"),
    path('perfil/', views.lista_r, name="perfil"),
    path('solicitudes/', views.mis_solicitudes, name="mis_solicitudes"),
    path("aplicar_ruta/", views.aplicar_ruta, name="aplicar_ruta"),
    path('miscalificaciones/', views.mis_calificaciones, name='mis_calificaciones'),
    path('misrutas/', views.misrutas, name="misrutas"),
    path("gestionar_solicitud/<int:solicitud_id>/", views.gestionar_solicitud, name="gestionar_solicitud"),
    path('alojamiento/', views.lista_residencias, name="lista_residencias"),
    path('index/', views.principal, name='principal'),
    path('principal/', views.pagprincipal, name='pagprincipal') ,
    path("login/", views.login_view, name="login"),
    path('ruta/<int:ruta_id>/cupos_dia/', views.get_cupos_dia, name='get_cupos_dia'),
    path('residencia/editar/<int:residencia_id>/', views.editar_residencia, name='editar_residencia'),
    path('residencia/eliminar/<int:residencia_id>/', views.eliminar_residencia, name='eliminar_residencia'),
    path("registro/", views.registro, name="registro"),
    path("rutas/", views.listar_rutas, name="listar_rutas"),
    path("crear_ruta/", views.crear_ruta, name="crear_ruta"),
    path("residencia/", views.alojamiento, name="rutas"),
    path('chat/<int:user_id>/', views.chat_privado, name='chat_privado'),  # Chat privado (inicia)
    path('api/mensajes/<int:chat_id>/', views.mensajes_chat, name='mensajes_chat'),  # API REST
    path('mis_chats/', views.mis_chats, name='mis_chats'), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
