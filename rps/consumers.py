import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from games.models import Room, ActiveUser, RPSMove
from common.models import LameUser
from django.db.models import Q
import random

class MinesweeperConsumer(WebsocketConsumer):
    def xy_to_pos(self, x, y):
        return (y * self.board.width) + x
    def pos_to_xy(self, pos):
        return (pos % self.board.width, pos // self.board.height)

    def send_client(self, tpy, msg):
        self.send(json.dumps({
            'type': tpy,
            'payload': msg
        }))

    def hit_bomb(self, sq):
        self.send_client('change-board', [{
            'x': sq.x,
            'y': sq.y,
            'flagged': sq.flagged,
            'bomb': sq.bomb,
            'bombs_next': sq.bombs_next
        }])
        self.lose()

    def client_selected_square(self, pos):
        x, y = self.pos_to_xy(pos)
        reved = self.reveal(x, y, [])
        print(reved)
        if len(reved) == 0:
            self.hit_bomb(self.board.cells.get(x=x, y=y))
        else:
            self.send_client('change-board', reved)
            self.save_revealed(reved)

    def check_win(self):
        if self.has_won():
            self.win()

    def has_won(self):
        shown = list(self.board.cells.filter(shown=True))
        not_bombs = list(self.board.cells.filter(bomb=False))
        return shown == not_bombs

    def win(self):
        self.send_client('message', '<b>You win!</b>')
        self.board.status = self.board.Status.WON
        self.board.save()

    def send_new_board(self):
        self.send_client('new_board', '')
        self.send_client('message', '<i>New board generated!</i>')

    def flag_tile(self, pos):
        x, y = self.pos_to_xy(pos)
        cell = MinesweeperCell.objects.get(x=x, y=y, board=self.board)
        if not cell.flagged:
            cell.shown = False
        cell.flagged = not cell.flagged
        cell.save()

    def send_shown_flagged(self):
        if (self.board.is_game_over()):
            self.send_client('change-board', [
                x.as_full_dict() for x in self.board.cells.all()
            ])
        else:
            shown = [{'x': x.x, 'y': x.y, 'bombs_next': x.bombs_next} for x in list(self.board.cells.filter(shown=True))]
            flagged = [{'x': x.x, 'y': x.y, 'flagged': True} for x in list(self.board.cells.filter(flagged=True))]
            self.send_client('change-board', shown + flagged)

    def save_revealed(self, revealed_squares):
        # edit database so user can come back later
        for cell in revealed_squares:
            dbcell = MinesweeperCell.objects.get(x=cell['x'], y=cell['y'], board=self.board)
            dbcell.shown = True
            dbcell.flagged = False
            dbcell.save()

    def valid_pos(self, x, y):
        return x >= 0 and x < self.board.width and y >= 0 and y < self.board.height

    def reveal(self, x, y, already_revealed):
        if not self.valid_pos(x, y):
            return already_revealed
        # if already checked
        for rev in already_revealed:
            if rev['x'] == x and rev['y'] == y:
                return already_revealed

        tile = self.board.cells.get(x=x, y=y)
        # if is bomb
        if tile.bomb:
            return already_revealed
        elif tile.bombs_next > 0:
            already_revealed.append({
                'x': x,
                'y': y,
                'bombs_next': self.cells[y][x]
            })
            return already_revealed
        # if bombs_next is 0
        already_revealed.append({
            'x': x,
            'y': y,
            'bombs_next': 0
        })

        for xd in range(-1, 2):
            for yd in range(-1, 2):
                nx = x+xd
                ny = y+yd
                # jump over middle square
                if nx == x and ny == y:
                    continue
                self.reveal(nx, ny, already_revealed)
        return already_revealed

    def select_board_if_exists(self):
        # if user has a board already available: use it instead
        current_board = MinesweeperBoard.objects.filter(user=self.user)
        if len(current_board) > 0:
            self.board = current_board[0]
            self.cells = [[0 for _ in range(self.board.width)] for _ in range(self.board.height)]
            for cell in self.board.cells.all():
               self.cells[cell.y][cell.x] = '*' if cell.bomb else cell.bombs_next
            return True
        self.board_generator()

    # TODO: make more efficient
    # TODO: make easier to read
    # TODO: Move to seperate file 
    def board_generator(self):
        self.board = MinesweeperBoard.objects.create(user=self.user)
        self.cells = []
        for y in range(self.board.height):
            self.cells.append([])
            for x in range(self.board.width):
                self.cells[y].append(0)
        placed_bombs = 0
        while placed_bombs < 15:
            rand = random.randint(0, (self.board.width * self.board.height)-1)

            x = rand % 10
            y = rand // 10
            if self.cells[y][x] != '*':
                self.cells[y][x] = '*'
                placed_bombs += 1
        for y in range(self.board.height):
            for x in range(self.board.width):
                i = (y*self.board.width) + x
                if self.cells[y][x] != '*':
                    # This finds the number of bombs within the 8 squares surrounding
                    check_matrix = [
                        (-1, -1),
                        (-1, 0),
                        (-1, 1),
                        (0, -1),
                        (0, 1),
                        (1, -1),
                        (1, 0),
                        (1, 1)
                    ]
                    bombs_around = 0
                    for p,q in check_matrix:
                        if self.valid_pos(p+y, q+x):
                            if self.cells[y+p][x+q] == '*':
                                bombs_around += 1
                    self.cells[y][x] = bombs_around
                m = MinesweeperCell.objects.create(
                    x=x,
                    y=y,
                    bombs_next=self.cells[y][x] if self.cells[y][x] != '*' else 0,
                    bomb=self.cells[y][x] == '*',
                    board=self.board,
                    shown=False
                )
    def lose(self):
        self.send_client('message', '<b>You hit a bomb!</b>')
        self.board.status = self.board.Status.LOST
        # This will remove all flags; I believe this is the classic behaviour
        self.board.cells.all().update(flagged=False)
        self.board.save()
        self.send_shown_flagged()

    def connect(self):
        self.accept()
        self.user = LameUser.objects.get(username=self.scope['user'].username)
        self.select_board_if_exists()
        self.send_shown_flagged()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'generate':
            self.board.delete()
            self.send_new_board()
            self.board_generator()
        elif data['type'] == 'clicked' and not self.board.is_game_over():
            self.client_selected_square(data['button_id'])
            self.check_win()
        elif data['type'] == 'flagged' and not self.board.is_game_over():
            self.flag_tile(data['button_id'])

class RPSConsumer(WebsocketConsumer):
    def group_send(self, message, event='info'):
        async_to_sync(self.channel_layer.group_send)(
            self.id,
            {
                'type': 'send_all',
                'event': event,
                'message': message
            }
        )

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
            self.room = Room.objects.create(id=self.room_id, game=self.game_name, game_name="Rock, Paper, Scissors")
            self.room.save()
            print("New Room")
        # Remove user from any old rooms
        ActiveUser.objects.filter(user=self.scope['user']).delete()

        # Add user to the new/existing room
        self.active_user = ActiveUser.objects.create(user=self.scope['user'], channel=self.channel_name, room=self.room)

        self.id = self.scope['url_route']['kwargs']['id']
        # tell everyone who will join on the next line :)
        self.group_send("{0} joined!".format(self.scope['user'].username))
        # add group channel
        async_to_sync(self.channel_layer.group_add)(
            self.id,
            self.channel_name
        )
        self.accept()
    
    def disconnect(self, close_code):
        self.active_user.delete()
        print("Deleted user")
        # Remove room if no more active users in room
        if len(self.room.active_users.all()) == 0:
            self.room.delete()
            print("Deleted room")
        
        self.group_send("{0} left!".format(self.scope['user'].username))
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
            self.group_send('tie', event='game_over')
        else:
            # TODO: Make cleaner; weird to do user.user
            self.group_send("{0} played {1}.<br>{2} played {3}.<br>{4} won!".format(moves[0].user.user.username, moves[0].choice, moves[1].user.user.username, moves[1].choice, moves[winner-1].user.user.username), event='game_over')

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
            move = RPSMove.objects.create(room=self.room, user=self.active_user, choice=choice)
            self.group_send("{0} has played!".format(self.scope['user'].username))
        elif len(moves_for_room) == 1:
            # if only one other move was made, and it was made by somebody else
            if moves_for_room[0].user != self.active_user:
                move = RPSMove.objects.create(room=self.room, user=self.active_user, choice=choice)
                self.game_over()
                self.clear_moves()
            else:
                self.already_made_move()
        else:
            # two or more moves defined: must clear all of them... shouldn't be run in theory
            self.clear_moves()

    def send_all(self, event):
        self.send(text_data=json.dumps(
            {
                'event': event['event'],
                'message': event['message']
            }
        ))
