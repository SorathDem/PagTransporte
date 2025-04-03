from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()  # Solo texto, sin emojis
    timestamp = models.DateTimeField(auto_now_add=True)  # Fecha y hora del mensaje

    class Meta:
        ordering = ["timestamp"]  # Ordenar por fecha de envío

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content}"


class Residencia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    ubicacion = models.URLField(max_length=500)
    
class ResidenciaImagen(models.Model):
    residencia = models.ForeignKey(Residencia, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='residencias/')

class Ruta(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    vehiculo = models.CharField(max_length=50, choices=[('Carro', 'Carro'), ('Moto', 'Moto')])
    cupos = models.IntegerField(default=1)  # Asegúrate de definir un valor por defecto
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Si el usuario puede ser opcional

    def __str__(self):
        return self.title
    
class CupoDia(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name="cupos_dia")
    dia = models.CharField(max_length=20)
    hora_ida = models.TimeField()
    cupos_ida = models.IntegerField()
    hora_vuelta = models.TimeField()
    cupos_vuelta = models.IntegerField()

    def __str__(self):
        return f"{self.ruta.title} - {self.dia}"

class Solicitud(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name="solicitudes")
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    dia = models.CharField(max_length=20)  # Este campo es para almacenar el día, podrías usar DateField si quieres almacenar fechas en lugar de texto.
    tipo_viaje = models.CharField(
        max_length=10, 
        choices=[("ida", "Solo ida"), ("vuelta", "Solo vuelta"), ("ambos", "Ida y vuelta")]
    )
    estado = models.CharField(
        max_length=20, 
        choices=[("pendiente", "Pendiente"), ("aceptado", "Aceptado"), ("rechazado", "Rechazado")],
        default="pendiente"
    )

    def __str__(self):
        return f"{self.estudiante} - {self.ruta} - {self.dia}"
    

class Calificacion(models.Model):
    usuario = models.ForeignKey(User, related_name='calificaciones_emitidas', on_delete=models.CASCADE)
    calificado_usuario = models.ForeignKey(User, related_name='calificaciones_recibidas', on_delete=models.CASCADE)
    estrellas = models.PositiveIntegerField(choices=[(1, '1 estrella'), (2, '2 estrellas'), (3, '3 estrellas'), (4, '4 estrellas'), (5, '5 estrellas')])
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['usuario', 'calificado_usuario']

    def __str__(self):
        return f'Calificación de {self.usuario.username} a {self.calificado_usuario.username}'