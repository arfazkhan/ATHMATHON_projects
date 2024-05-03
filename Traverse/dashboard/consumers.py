from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.utils.timezone import datetime
from .models import Chat, GroupChat, TravelPlanTrip
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.receiver = None
        self.group_name = None
        self.user = None

    def connect(self):
        print("Hi")
        self.accept()
        print("Connected...")
        self.receiver = User.objects.get(
            username=self.scope['url_route']['kwargs']['username'])
        self.user = self.scope['user']

        if int(self.user.id < self.receiver.id):
            self.group_name = 'chat_' + self.user.username + '_' + self.receiver.username
        else:
            self.group_name = 'chat_' + self.receiver.username + '_' + self.user.username

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        print(f"Connected to chat: {self.scope['user']}, {self.receiver}")


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if not self.scope['user'].is_authenticated:
            return

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat',
                'user': str(self.scope['user'].username),
                # %Y-%m-%d |
                'timestamp': str(datetime.now().strftime('%H:%M')),
                'message': message
            }
        )
        receiver = User.objects.get(username=self.receiver)
        Chat.objects.create(
            message=message, sender=self.scope['user'], receiver=receiver)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def chat(self, event):
        self.send(text_data=json.dumps(event))


class GroupChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.user = None

    def connect(self):
        self.accept()
        self.user = self.scope['user']
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'connected',
                'message': f"Connected To {self.group_name}",
                'timestamp': str(datetime.now().strftime('%H:%M')),
            }
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if not self.scope['user'].is_authenticated:
            return

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat',
                'user': str(self.scope['user'].username),
                'timestamp': str(datetime.now().strftime('%H:%M')),
                'message': message
            }
        )
        GroupChat.objects.create(
            message=message, sender=self.scope['user'], receiver=TravelPlanTrip.objects.get(group_name=self.scope['url_route']['kwargs']['group_name']))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def chat(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'timestamp': str(datetime.now().strftime('%H:%M')),
        }))

    def connected(self, event):
        self.send(text_data=json.dumps(event))