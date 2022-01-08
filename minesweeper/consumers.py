import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
# TODO: rename
from games.models import MinesweeperBoard, MinesweeperCell
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

