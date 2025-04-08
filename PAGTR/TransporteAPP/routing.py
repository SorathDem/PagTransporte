from django.urls import path
from TransporteAPP.consumers import ChatConsumer
from . import consumers

websocket_urlpatterns = [
    path("ws/chat/", ChatConsumer.as_asgi()),
    path('ws/some_path/', consumers.MyConsumer.as_asgi()),
]
