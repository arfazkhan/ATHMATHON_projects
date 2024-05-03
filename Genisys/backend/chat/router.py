from django.urls import path
from . import consumer


websocket_urlpatterns = [
    path('ws/server/', consumer.chatConsumer.as_asgi())
]