from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from .models import Message
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Residencia
from .models import Ruta, Solicitud
from .models import Residencia, ResidenciaImagen
from .forms import ResidenciaForm, ResidenciaImagenForm
from .forms import RutaForm , CupoPorDiaFormSet
from django.contrib import messages
from .forms import RutaForm, CupoPorDiaForm 
from .forms import AplicarRutaForm
from .models import Calificacion
from .forms import CalificacionForm
from django.db.models import Avg
from django.db.models import Q
# Create your views here.
@login_required
def login_page(request):
   return render(request, 'login.html')

def principal(request):
    return render(request, "index.html")

def chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    return render(request, 'chat.html', {'chat': chat, 'user': request.user})

def detalle_ruta(request, ruta_id):
    ruta = get_object_or_404(Ruta, id=ruta_id)  # Obtener la ruta
    usuario_creador = ruta.creador  # Obtener el usuario que la creó

    return render(request, 'ruta_detalle.html', {'ruta': ruta, 'usuario_creador': usuario_creador})

def perfil_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    
    # Verificar si el usuario ya ha calificado a este perfil
    if request.user.is_authenticated:
        ya_califico = Calificacion.objects.filter(usuario=request.user, calificado_usuario=usuario).exists()
    else:
        ya_califico = False

    # Si el usuario envía una calificación, la guardamos
    if request.method == 'POST' and not ya_califico:
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.usuario = request.user
            calificacion.calificado_usuario = usuario
            calificacion.save()
            return redirect('perfil_usuario', usuario_id=usuario.id)  # Redirigir para evitar el reenvío del formulario
    else:
        form = CalificacionForm()

    return render(request, 'perfil_usuario.html', {
        'usuario': usuario,
        'form': form,
        'ya_califico': ya_califico
    })
    
# views.py
from django.shortcuts import render
from .models import Calificacion
from django.contrib.auth.models import User

def mis_calificaciones(request):
    # Obtener el usuario logueado
    usuario = request.user

    # Obtener todas las calificaciones que ha recibido el usuario
    calificaciones = Calificacion.objects.filter(calificado_usuario=usuario)

    # Agregar range a cada calificación antes de enviarlo a la plantilla
    for calificacion in calificaciones:
        calificacion.range_estrellas = range(calificacion.estrellas)

    # Calcular el promedio de calificación
    promedio = calificaciones.aggregate(Avg('estrellas'))['estrellas__avg'] or 0

    return render(request, 'miscalificaciones.html', {'calificaciones': calificaciones, 'promedio': promedio})


@login_required
def mis_solicitudes(request):
    solicitudes = Solicitud.objects.filter(estudiante=request.user)
    return render(request, 'missolicitudes.html', {'solicitudes': solicitudes})

def misrutas(request):
    rutas = Ruta.objects.filter(usuario=request.user)  # Filtra rutas del usuario actual
    return render(request, "misrutas.html", {"rutas": rutas})

def perfil(request):
    return render(request, "perfil.html")

def edit_rut(request):
    return render(request, "editar_ruta.html")

@login_required
def pagprincipal(request):
    return render(request, "pagPrincipal.html")

def alojamiento(request):
    return render(request, "alojamiento.html")

def redirigir_usuario(request):
    if request.user.is_superuser:
        return redirect('pagPrincipal')  # Redirige al panel de administración
    elif request.user.is_staff:
        return redirect('psicologo')  # Redirige a la página de psicólogos
    else:
        return redirect('pagPrincipal.html')  # Redirige a la página de usuario normal
    
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirigir_usuario(request)  # Redirige según el tipo de usuario
        else:
            return render(request, "login.html", {"error": "Usuario o contraseña incorrectos"})  

    return render(request, "login.html")

def registro(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/accounts/login/")
    else:
        form = CustomUserCreationForm()

    return render(request, "registro.html", {"form": form})

@login_required
def chat_view(request, object_type, object_id):
    """
    Vista para el chat, permitiendo acceder dependiendo del tipo de objeto (ruta o residencia).
    """
    if object_type == "ruta":
        obj = get_object_or_404(Ruta, id=object_id)
        receiver = obj.usuario  # Asegurar que Ruta tiene un campo usuario
    elif object_type == "residencia":
        obj = get_object_or_404(Residencia, id=object_id)
        receiver = obj.usuario  # Asegurar que Residencia tiene un campo usuario
    else:
        return render(request, "error.html", {"error": "Tipo de objeto inválido"})

    messages = Message.objects.filter(
        sender=request.user, receiver=receiver
    ) | Message.objects.filter(
        sender=receiver, receiver=request.user
    ).order_by("timestamp")

    return render(request, "chat.html", {"receiver": receiver, "messages": messages})

API_KEY = "TU_API_KEY"

def obtener_coordenadas(direccion):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        return data['results'][0]['geometry']['location']
    return None

from django.shortcuts import render, redirect
from .models import Ruta, CupoDia

def crear_ruta(request):
    if request.method == "POST":
        titulo = request.POST.get("title")
        descripcion = request.POST.get("description")
        vehiculo = request.POST.get("vehiculo")
        cupos_totales = request.POST.get("cupos")
        municipio_ruta = request.POST.get("municipio_ruta")
        
        # Crear la ruta en la base de datos
        ruta = Ruta.objects.create(
            title=titulo,  # Usar la variable obtenida en lugar de `form.cleaned_data`
            description=descripcion,
            vehiculo=vehiculo,
            cupos=cupos_totales,
            usuario=request.user,
            municipio_ruta=municipio_ruta,
        )

        # Guardar los cupos por día
        dias = request.POST.getlist("dia[]")
        horas_ida = request.POST.getlist("hora_ida[]")
        cupos_ida = request.POST.getlist("cupos_ida[]")
        horas_vuelta = request.POST.getlist("hora_vuelta[]")
        cupos_vuelta = request.POST.getlist("cupos_vuelta[]")

        for i in range(len(dias)):
            CupoDia.objects.create(
                ruta=ruta,
                dia=dias[i],
                hora_ida=horas_ida[i],
                cupos_ida=cupos_ida[i],
                hora_vuelta=horas_vuelta[i],
                cupos_vuelta=cupos_vuelta[i]
            )

        return redirect("/misrutas/")  # Reemplaza con la vista a la que quieres redirigir

    return render(request, "crear_ruta.html")

def listar_rutas(request):
    rutas = Ruta.objects.all()  # Obtener todas las rutas de la base de datos
    return render(request, 'rutas.html', {'rutas': rutas, 'usuario_id': request.user.id})

def listar_rut(request):
    rutas = Ruta.objects.prefetch_related("cupos_dia").all() # Obtener todas las rutas de la base de datos
    return render(request, 'perfil.html', {'rutas': rutas})

from django.shortcuts import render
from .models import Residencia

def residencias(request):
    residencias = Residencia.objects.all()
    return render(request, 'alojamiento.html', {'residencias': residencias})

def lista_residencias(request):
    residencias = Residencia.objects.all()
    return render(request, "alojamiento.html", {"residencias": residencias})

def lista_r(request):
    residencias = Residencia.objects.filter(usuario=request.user)
    return render(request, "perfil.html", {"residencias": residencias})

def crear_residencia(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        ubicacion = request.POST['ubicacion']
        municipio = request.POST['municipio']
        
        nueva_residencia = Residencia.objects.create(
            usuario=request.user,
            titulo=titulo,
            descripcion=descripcion,
            ubicacion=ubicacion,
            municipio=municipio,
        )
        
        # Guardar múltiples imágenes
        for imagen in request.FILES.getlist('imagenes'):
            ResidenciaImagen.objects.create(residencia=nueva_residencia, imagen=imagen)

        return redirect('/alojamiento/')

    return render(request, 'alojamiento.html')

def crear_r(request):
    if request.method == "POST":
        residencia_form = ResidenciaForm(request.POST)
        imagen_form = ResidenciaImagenForm(request.POST, request.FILES)

        if residencia_form.is_valid() and imagen_form.is_valid():
            residencia = residencia_form.save(commit=False)
            residencia.usuario = request.user  # Asignamos el usuario actual
            residencia.save()

            imagen = imagen_form.save(commit=False)
            imagen.residencia = residencia  # Asociamos la imagen con la residencia creada
            imagen.save()

            return redirect('/perfi/')  # Redirigir a donde necesites

    else:
        residencia_form = ResidenciaForm()
        imagen_form = ResidenciaImagenForm()

    return render(request, 'tu_template.html', {
        'residencia_form': residencia_form,
        'imagen_form': imagen_form
    })

def editar_residencia(request, residencia_id):
    residencia = get_object_or_404(Residencia, id=residencia_id, usuario=request.user)
    
    if request.method == "POST":
        form = ResidenciaForm(request.POST, request.FILES, instance=residencia)
        if form.is_valid():
            form.save()
            return redirect('/perfil/')  # Redirige a la lista de residencias
    else:
        form = ResidenciaForm(instance=residencia)

    return render(request, 'editar_residencia.html', {'form': form, 'residencia': residencia})

# Vista para eliminar una residencia
@login_required
def eliminar_residencia(request, residencia_id):
    residencia = get_object_or_404(Residencia, id=residencia_id, usuario=request.user)
    
    if request.method == "POST":
        residencia.delete()
        return redirect('/perfil/')

    return render(request, 'confirmar_eliminar.html', {'residencia': residencia})

@login_required
def editar_ruta(request, ruta_id):
    ruta = get_object_or_404(Ruta, id=ruta_id, usuario=request.user)

    # Si el formulario fue enviado (POST)
    if request.method == 'POST':
        # Creamos el formulario para la ruta
        form = RutaForm(request.POST, instance=ruta)
        # Creamos el formset para los cupos por día
        formset = CupoPorDiaFormSet(request.POST, instance=ruta)

        # Si ambos formularios son válidos
        if form.is_valid() and formset.is_valid():
            form.save()  # Guardamos los cambios en la ruta
            formset.save()  # Guardamos los cambios en los cupos por día
            return redirect('misrutas')  # Redirigir al listado de rutas (ajusta la url según corresponda)

    else:
        # Si la solicitud es GET, creamos el formulario para la ruta y el formset para los cupos
        form = RutaForm(instance=ruta)
        formset = CupoPorDiaFormSet(instance=ruta)

    return render(request, 'editar_ruta.html', {
        'form': form,
        'formset': formset,
        'ruta': ruta
    })

@login_required
def eliminar_ruta(request, ruta_id):
    ruta = get_object_or_404(Ruta, id=ruta_id, usuario=request.user)

    if request.method == 'POST':
        ruta.delete()  # Eliminar la ruta
        return redirect('misrutas')  # Redirigir al listado de rutas

    return render(request, 'confirmar_eliminar_ruta.html', {'ruta': ruta})


@login_required
def aplicar_ruta(request):
    if request.method == "POST":
        # Instancia el formulario con los datos del POST
        form = AplicarRutaForm(request.POST)

        if form.is_valid():
            # Obtiene los datos validados
            dia = form.cleaned_data['dia']
            tipo_viaje = form.cleaned_data['tipo_viaje']
            ruta_id = request.POST.get("ruta_id")

            # Recupera la ruta seleccionada
            ruta = get_object_or_404(Ruta, id=ruta_id)

            # Crea una nueva solicitud
            solicitud = Solicitud(
                estudiante=request.user,
                ruta=ruta,
                dia=dia,
                tipo_viaje=tipo_viaje
            )

            # Guarda la solicitud en la base de datos
            solicitud.save()

            # Redirige a la página de perfil o donde desees
            return redirect("perfil")
    else:
        # Si es un GET, muestra el formulario vacío
        ruta_id = request.GET.get("ruta_id")
        ruta = get_object_or_404(Ruta, id=ruta_id)

        # Obtiene los cupos disponibles para la ruta
        cupos_dia = ruta.cupos_dia.all()

        # Crea una instancia vacía del formulario
        form = AplicarRutaForm()

        # Pasa los datos al contexto
        return render(request, "rutas.html", {
            "ruta": ruta,
            "cupos_dia": cupos_dia,
            "form": form  # Asegúrate de pasar el formulario al contexto
        })

@login_required
def gestionar_solicitud(request, solicitud_id):
    # Obtener la solicitud
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    if request.method == "POST":
        accion = request.POST.get("accion")
        
        # Cambiar el estado de la solicitud
        if accion == "aceptar":
            solicitud.estado = "aceptado"
            # Actualizar los cupos si es aceptada
            ruta = solicitud.ruta
            cupo = ruta.cupos_dia.filter(dia=solicitud.dia).first()  # Encontrar el cupo correspondiente al día
            if cupo:
                if cupo.cupos_ida > 0:
                    cupo.cupos_ida -= 1  # Reducir el cupo de ida
                    cupo.save()
                else:
                    # Si no hay cupos disponibles, agregar mensaje o manejar el caso
                    solicitud.estado = "rechazado"  # O podría ser "pendiente" si prefieres mantenerlo
                    solicitud.save()
                    return render(request, "error_no_cupo.html", {"mensaje": "No hay cupos disponibles para esta fecha."})
        elif accion == "rechazar":
            solicitud.estado = "rechazado"

        # Guardar los cambios de estado
        solicitud.save()

        return redirect("perfil")  # Redirigir a la vista donde se muestran las solicitudes

    # Si el método no es POST, redirigir
    return redirect("solicitudes")

def get_cupos_dia(request, ruta_id):
    ruta = get_object_or_404(Ruta, id=ruta_id)
    cupos_dia = ruta.cupos_dia.all().values('dia')  # Solo recuperamos los días
    return JsonResponse({'cupos_dia': list(cupos_dia)})

from django.urls import reverse

def rutas(request):
    usuario = request.user  # O la forma en que obtienes al usuario
    if usuario.id:
        perfil_url = reverse('perfil_usuario', args=[usuario.id])
    else:
        perfil_url = "#"
    return render(request, 'rutas.html', {'usuario': usuario, 'perfil_url': perfil_url})

from .forms import MensajeForm
from .models import Mensaje


def chat_privado(request, user_id):
    user_destino = get_object_or_404(User, id=user_id)
    user_actual = request.user

    # Buscar si ya existe un chat entre ellos
    chat = Chat.objects.filter(participantes=user_actual).filter(participantes=user_destino).first()

    if not chat:
        # Si no existe, crear un nuevo chat
        chat = Chat.objects.create()
        chat.participantes.add(user_actual, user_destino)
        chat.save()

    # Redirigir al template del chat, pasándole el chat_id
    return render(request, 'chat.html', {'chat': chat, 'user': request.user})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Mensaje, Chat  # Ajusta a tus modelos

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Chat, Mensaje
import json

@csrf_exempt
def mensajes_chat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)

    if request.method == 'GET':
        mensajes = chat.mensajes.select_related('remitente').order_by('fecha_creacion')
        data = [{
            'id': mensaje.id,
            'remitente': mensaje.remitente.username,
            'texto': mensaje.texto,
            'fecha_creacion': mensaje.fecha_creacion.isoformat()
        } for mensaje in mensajes]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        body = json.loads(request.body)
        texto = body['texto']
        remitente_id = body['remitente_id']

        remitente = User.objects.get(id=remitente_id)

        mensaje = Mensaje.objects.create(chat=chat, remitente=remitente, texto=texto)
        return JsonResponse({'success': True, 'mensaje_id': mensaje.id})

def mis_chats(request):
    chats = request.user.chats.all()

    chats_con_otros = []
    for chat in chats:
        otros = chat.participantes.exclude(id=request.user.id)
        if otros.exists():
            chats_con_otros.append({
                'chat': chat,
                'otro_participante': otros.first()
            })

    return render(request, 'mis_chats.html', {
        'chats_con_otros': chats_con_otros,
    })

