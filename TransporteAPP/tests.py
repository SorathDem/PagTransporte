from django.test import TestCase
from django.contrib.auth.models import User
from TransporteAPP.models import Residencia, Ruta, Message, Calificacion, Solicitud, CupoDia

class ResidenciaTestCase(TestCase):
    def setUp(self):
        """ Configura datos antes de cada prueba """
        self.user = User.objects.create_user(username="usuario_test", password="123456")
        self.residencia = Residencia.objects.create(
            usuario=self.user,
            titulo="Casa Azul",
            descripcion="Bonita casa en la ciudad",
            ubicacion="https://maps.google.com"
        )

    def test_crear_residencia(self):
        """ Verifica que se creó la residencia correctamente """
        residencia = Residencia.objects.get(titulo="Casa Azul")
        self.assertEqual(residencia.usuario.username, "usuario_test")

class RutaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="conductor", password="123456")
        self.ruta = Ruta.objects.create(
            usuario=self.user,
            title="Ruta Universitaria",
            description="Viaje de la ciudad a la universidad",
            vehiculo="Carro",
            cupos=4
        )

    def test_crear_ruta(self):
        """ Verifica que la ruta fue creada correctamente """
        ruta = Ruta.objects.get(title="Ruta Universitaria")
        self.assertEqual(ruta.vehiculo, "Carro")
        self.assertEqual(ruta.cupos, 4)

class MessageTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="usuario1", password="123456")
        self.user2 = User.objects.create_user(username="usuario2", password="123456")
        self.mensaje = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hola, ¿cómo estás?"
        )

    def test_mensaje_creado(self):
        """ Verifica que el mensaje fue creado correctamente """
        mensaje = Message.objects.get(sender=self.user1)
        self.assertEqual(mensaje.content, "Hola, ¿cómo estás?")

class CalificacionTestCase(TestCase):
    def setUp(self):
        self.usuario1 = User.objects.create_user(username="usuario1", password="123456")
        self.usuario2 = User.objects.create_user(username="usuario2", password="123456")
        self.calificacion = Calificacion.objects.create(
            usuario=self.usuario1,
            calificado_usuario=self.usuario2,
            estrellas=5,
            comentario="Excelente servicio"
        )

    def test_calificacion_creada(self):
        """ Verifica que la calificación fue creada correctamente """
        calificacion = Calificacion.objects.get(usuario=self.usuario1)
        self.assertEqual(calificacion.estrellas, 5)
        self.assertEqual(calificacion.comentario, "Excelente servicio")

class SolicitudTestCase(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="estudiante", password="123456")
        self.ruta = Ruta.objects.create(
            usuario=self.usuario,
            title="Ruta a la universidad",
            description="Viaje desde casa hasta la universidad",
            vehiculo="Moto",
            cupos=2
        )
        self.solicitud = Solicitud.objects.create(
            estudiante=self.usuario,
            ruta=self.ruta,
            dia="Lunes",
            tipo_viaje="ida",
            estado="pendiente"
        )

    def test_solicitud_creada(self):
        """ Verifica que la solicitud fue creada correctamente """
        solicitud = Solicitud.objects.get(estudiante=self.usuario)
        self.assertEqual(solicitud.tipo_viaje, "ida")
        self.assertEqual(solicitud.estado, "pendiente")

class CupoDiaTestCase(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="conductor", password="123456")
        self.ruta = Ruta.objects.create(
            usuario=self.usuario,
            title="Ruta a la U",
            description="Viaje matutino",
            vehiculo="Carro",
            cupos=3
        )
        self.cupo_dia = CupoDia.objects.create(
            ruta=self.ruta,
            dia="Martes",
            hora_ida="07:30",
            cupos_ida=2,
            hora_vuelta="18:00",
            cupos_vuelta=1
        )

    def test_cupo_dia_creado(self):
        """ Verifica que los cupos del día fueron creados correctamente """
        cupo = CupoDia.objects.get(ruta=self.ruta)
        self.assertEqual(cupo.dia, "Martes")
        self.assertEqual(cupo.cupos_ida, 2)
        self.assertEqual(cupo.cupos_vuelta, 1)
