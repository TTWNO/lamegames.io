import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Room, ActiveUser

class RPSConsumer(WebsocketConsumer):
    def connect(self):
        self.host_user = self.scope['user'].username
        async_to_sync(self.channel_layer.group_add)(
            self.host_user,
            self.channel_name
        )
        self.room = Room(game="rps")
        self.active_user = ActiveUser(username=self.host_user, room=self.room)
        self.room.save()
        self.active_user.save()
        
        self.accept()
    
    def disconnect(self, close_code):
        self.room.delete()
        async_to_sync(self.channel_layer.group_discard)(
            self.host_user,
            self.channel_name
        )

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.host_user,
            {
                'type': 'test',
                'message': 'pong'
            }
        )
    
    def test(self, event):
        rooms = []
        for room in Room.objects.all():
            add_to_rooms = dict()
            add_to_rooms['game'] = room.game
            add_to_rooms['people'] = []
            for user in ActiveUser.objects.filter(room=room):
                add_to_rooms['people'].append(user.username)
            rooms.append(add_to_rooms)

        self.send(text_data=json.dumps(
            {
                'message': event['message'],
                'stuff': rooms
            }
        ))