import json
from django.db import models

# Create your models here.

class Room(models.Model):
    game = models.CharField(max_length=32)

    def toJson(self):
        return JSON.dumps({'game': self.game})

class ActiveUser(models.Model):
    username = models.CharField(max_length=32)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
