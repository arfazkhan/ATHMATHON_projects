import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from dashboard.consumers import ChatConsumer, GroupChatConsumer
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter([
        path('ws/chat/<str:username>/', ChatConsumer.as_asgi()),
        path('ws/chat/group/<str:group_name>/',
             GroupChatConsumer.as_asgi()),
    ])),
})
