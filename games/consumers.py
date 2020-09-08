import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Room, ActiveUser, RPSMove

class RPSConsumer(WebsocketConsumer):
    def connect(self):
        self.game_name = "RPS"

        # Check if room with ID already exists
        self.room_id = self.scope['path'].split('/')[-1]
        rooms_with_id = Room.objects.filter(id=self.room_id)
        # Add user to room if it already exists
        if len(rooms_with_id) > 0:
            self.room = rooms_with_id[0]
            print("Room Aleady Available")
        # create new room if not exists
        else:
            self.room = Room.objects.create(id=self.room_id, game=self.game_name)
            self.room.save()
            print("New Room")
        # Add user to the new/existing room
        self.active_user = ActiveUser.objects.create(username=self.scope['user'].username, channel=self.channel_name, room=self.room)

        self.id = self.scope['url_route']['kwargs']['id']
        # add group channel
        async_to_sync(self.channel_layer.group_add)(
            self.id,
            self.channel_name
        )
        self.accept()
    
    def disconnect(self, close_code):
        self.active_user.delete()
        # Remove room if no more active users in room
        if len(self.room.active_users.all()) == 0:
            self.room.delete()
            print("Deleted room")
        
        # remove this (now defunct) socket from the channel layer gorup
        async_to_sync(self.channel_layer.group_discard)(
            self.id,
            self.channel_name
        )

    def game_over(self):
        moves = RPSMove.objects.filter(room=self.room)
        move1c = moves[0].choice
        move2c = moves[1].choice
        winner = 0

        if move1c == "rock":
            if move2c == "rock":
                pass
            elif move2c == "paper":
                winner = 2
            elif move2c == "scissors":
                winner = 1
        elif move1c == "paper":
            if move2c == "rock":
                winner = 1
            elif move2c == "paper":
                pass
            elif move2c == "scissors":
                winner = 2
        elif move1c == "scissors":
            if move2c == "rock":
                winner = 2
            elif move2c == "paper":
                winner = 1
            elif move2c == "scissors":
                pass
        
        if winner == 0:
            async_to_sync(self.channel_layer.group_send)(
                self.id,
                {
                    'type': 'group_send',
                    'event': 'game_over',
                    'message': 'tie'
                }
            )
        elif winner == 1:
            async_to_sync(self.channel_layer.group_send)(
                self.id,
                {
                    'type': 'group_send',
                    'event': 'game_over',
                    'message': {'winner': moves[0].user.username},
                }
            )
        elif winner == 2:
            async_to_sync(self.channel_layer.group_send)(
                self.id,
                {
                    'type': 'group_send',
                    'event': 'game_over',
                    'message': {'winner': moves[1].user.username}
                }
            )

    def already_made_move(self):
        self.send(text_data=json.dumps({
            'event': 'warning',
            'message': "You have already submitted you move. Wait for your opponent!"
        }))

    def clear_moves(self):
        # remove all moves associated with room
        RPSMove.objects.filter(room=self.room).delete()

    def receive(self, text_data):
        choice = json.loads(text_data)['choice']
        moves_for_room = RPSMove.objects.filter(room=self.room)
        # if no moves
        if len(moves_for_room) == 0:
            print("No moves")
            move = RPSMove.objects.create(room=self.room, user=self.active_user, choice=choice)
            print("Adding one move")
        elif len(moves_for_room) == 1:
            print("One move")
            # if only one other move was made, and it was made by somebody else
            if moves_for_room[0].user != self.active_user:
                print("Other user did move.")
                move = RPSMove.objects.create(room=self.room, user=self.active_user, choice=choice)
                print("Made move")
                self.game_over()
                self.clear_moves()
            else:
                self.already_made_move()
        else:
            # two or more moves defined: must clear all of them... shouldn't be run in theory
            self.clear_moves()

    def group_send(self, event):
        self.send(text_data=json.dumps(
            {
                'event': event['event'],
                'message': event['message']
            }
        ))