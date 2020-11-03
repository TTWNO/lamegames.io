from django.db import models

from games.models import Room
from common.models import LameUser

# Create your models here.
class BattleshipBoard(models.Model):
    pass

class BattleshipCell(models.Model):
    class Type(models.IntegerChoices):
        EMPTY = 0
        DESTORYER = 1
        SUBMARINE = 2
        CRUISER = 3
        BATTLESHIP = 4
        CARRIER = 5

    x = models.SmallIntegerField()
    y = models.SmallIntegerField()
    contents = models.IntegerField(choices=Type.choices, default=Type.EMPTY)
    shot = models.BooleanField()
    board = models.ForeignKeyField(BattleshipBoard, on_delete=models.CASCADE, related_name='cells')