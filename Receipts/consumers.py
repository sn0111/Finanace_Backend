# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatMessages


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'chat'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    def fetch_data(self,data):
        msgs = ChatMessages.objects.all()
        messages=[]
        for msg in msgs:
            messages.append({
                'message':msg.message,
                'name':msg.name,
                # 'time':msg.time.date()
            })
        self.send_chat_message(messages)

    def new_message(self,data):
        chat = ChatMessages.objects.create(message=data['message'],name=data['name'])
        self.send(text_data=json.dumps({
            'message': chat.message,
            'name': chat.name
        }))

    commands ={
        'get_data':fetch_data,
        'new':new_message
    }
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.commands[text_data_json['command']](self, text_data_json)

    def send_chat_message(self,message):
        # Send message to room group
        print("sending...")
        self.send(text_data=json.dumps({'message': message}))
    # def send_chat_message(self,text_data_json):
    #     message = text_data_json['message']
    #     name = text_data_json['name']
    #     chat = ChatMessages.objects.create(message=message,name=name)
    #     # print(chat.message)
    #
    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message,
    #             'name': name
    #         }
    #     )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        name = event['name']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'name': name
        }))
