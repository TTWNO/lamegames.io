from django.shortcuts import (
    render, HttpResponse, redirect
)
from django.urls import reverse
from .models import Room, ActiveUser, MinesweeperBoard

# Create your views here.
def rps(request):
    return render(request, 'games/rps/rps_choose.html', {})

def rps_select(request):
    return render(request, 'games/rps/rps_join.html', {'all_rooms': Room.objects.all()})

def rps_join(request, room_id):
    return render(request, 'games/rps/rps.html', {'ROOM_ID': room_id})

def rps_create(request):
    return redirect(reverse('rps/join', args=[request.user.username]))

def minesweeper(request):
    board = MinesweeperBoard.objects.filter(user=request.user)
    if len(board) > 0:
        board = board[0]
    else:
        board = MinesweeperBoard.objects.create(user=request.user)
    id_board = [[(y*board.width)+x for x in range(board.width)] for y in range(board.height)]
    return render(request, 'games/minesweeper/minesweeper.html', {
        'board': id_board
    })
