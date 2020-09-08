from django.shortcuts import (
    render, HttpResponse, redirect
)
from django.urls import reverse
from .models import Room, ActiveUser

# Create your views here.
def rps(request):
    return render(request, 'games/rps/rps_choose.html', {})

def rps_select(request):
    return render(request, 'games/rps/rps_join.html', {'all_rooms': Room.objects.all()})

def rps_join(request, room_id):
    return render(request, 'games/rps/rps.html', {'ROOM_ID': room_id})

def rps_create(request):
    username = request.user.username
    
    room = Room(game="rps", id=username)
    active_user = ActiveUser(username=username, room=room)
    room.save()
    active_user.save()

    return redirect(reverse('rps/join', args=[username]))