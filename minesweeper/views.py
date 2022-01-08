from django.shortcuts import (
    render, HttpResponse, redirect
)
from django.urls import reverse
# TODO: rename
from games.models import MinesweeperBoard

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
