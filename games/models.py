import json
from django.db import models
from common.models import LameUser

# Create your models here.

class Room(models.Model):
    game = models.CharField(max_length=32)
    game_name = models.CharField(max_length=32)
    id = models.CharField(max_length=64, primary_key=True)

    def toJson(self):
        return JSON.dumps({'game': self.game})

class ActiveUser(models.Model):
    user = models.OneToOneField(LameUser, on_delete=models.CASCADE)
    channel = models.CharField(max_length=128)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='active_users')

    def __str__(self):
        return self.user.username

class RPSMove(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(ActiveUser, on_delete=models.CASCADE)
    choice = models.CharField(max_length=8)

# Create your models here.
class MinesweeperBoard(models.Model):
    class Status(models.IntegerChoices):
        IN_PROGRESS = 0
        LOST = 1
        WON = 2
    
    user = models.OneToOneField(LameUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices, default=Status.IN_PROGRESS)
    width = models.SmallIntegerField(default=10)
    height = models.SmallIntegerField(default=10)
    bombs = models.SmallIntegerField(default=15)

    def is_game_over(self):
        return self.status in [self.Status.LOST, self.Status.WON]

class MinesweeperCell(models.Model):
    shown = models.BooleanField(default=False)
    bomb = models.BooleanField()
    flagged = models.BooleanField(default=False)
    bombs_next = models.SmallIntegerField()
    x = models.SmallIntegerField()
    y = models.SmallIntegerField()
    board = models.ForeignKey(MinesweeperBoard, on_delete=models.CASCADE, related_name='cells')

    # NOTE: For dev purposes only
    def __str__(self):
        return json.dumps({
            'x': self.x,
            'y': self.y,
            'flagged': self.flagged,
            'shown': self.shown,
            'bomb': self.bomb
        })

    def as_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'bombs_next': self.bombs_next,
            'flagged': self.flagged,
            'shown': self.shown
        }
    def as_full_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'bombs_next': self.bombs_next,
            'flagged': self.flagged,
            'shown': self.shown,
            'bomb': self.bomb
        }
