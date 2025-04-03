from django.contrib import admin

from django.contrib import admin
from .models import Message, Residencia, ResidenciaImagen, Ruta, CupoDia, Solicitud, Calificacion

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'content')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('timestamp',)

class ResidenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'ubicacion', 'usuario')
    search_fields = ('titulo', 'descripcion', 'ubicacion')
    list_filter = ('usuario',)

class ResidenciaImagenAdmin(admin.ModelAdmin):
    list_display = ('residencia', 'imagen')
    search_fields = ('residencia__titulo',)

class RutaAdmin(admin.ModelAdmin):
    list_display = ('title', 'vehiculo', 'cupos', 'usuario')
    search_fields = ('title', 'vehiculo', 'usuario__username')
    list_filter = ('vehiculo',)

class CupoDiaAdmin(admin.ModelAdmin):
    list_display = ('ruta', 'dia', 'hora_ida', 'cupos_ida', 'hora_vuelta', 'cupos_vuelta')
    search_fields = ('ruta__title', 'dia')
    list_filter = ('dia',)

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'ruta', 'dia', 'tipo_viaje', 'estado')
    search_fields = ('estudiante__username', 'ruta__title')
    list_filter = ('estado',)

class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'calificado_usuario', 'estrellas', 'comentario', 'fecha')
    search_fields = ('usuario__username', 'calificado_usuario__username', 'comentario')
    list_filter = ('estrellas', 'fecha')

# Registrar todos los modelos
admin.site.register(Message, MessageAdmin)
admin.site.register(Residencia, ResidenciaAdmin)
admin.site.register(ResidenciaImagen, ResidenciaImagenAdmin)
admin.site.register(Ruta, RutaAdmin)
admin.site.register(CupoDia, CupoDiaAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Calificacion, CalificacionAdmin)

