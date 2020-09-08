from django.shortcuts import (
    render, HttpResponse, redirect
)
from .models import *

# Create your views here.
def rps(request):
    return render(request, 'games/rps_choose.html', {})

def rps_join(request):
    if request.method == 'POST':
        return render(request, 'games/rps.html', {
            'ROOM_ID': request.POST['rid']
        })
    else:
        return render(request, 'games/rps_join.html', {})

def rps_create(request):
    username = request.user.username
    # if the current user is in another room. Remove them.
    for x in Room.objects.all():
        print("Checking room...")
        if len(ActiveUser.objects.filter(room=x, username=username)) > 0:
            print("User in another room. Deleting")
            x.delete()
    
    room = Room(game="rps", id=username)
    active_user = ActiveUser(username=username, room=room)
    room.save()
    active_user.save()

    return redirect('rps/join')