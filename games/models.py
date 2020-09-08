import json
from django.db import models

# Create your models here.

class Room(models.Model):
    game = models.CharField(max_length=32)
    id = models.CharField(max_length=64, primary_key=True)

    def toJson(self):
        return JSON.dumps({'game': self.game})

class ActiveUser(models.Model):
    username = models.CharField(max_length=32)
    channel = models.CharField(max_length=128)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='active_users')

class RPSMove(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(ActiveUser, on_delete=models.CASCADE)
    choice = models.CharField(max_length=8)

