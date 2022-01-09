from django.urls import path
from . import views
from . import consumers

urlpatterns = [
    path('minesweeper/', views.minesweeper, name='minesweeper')
]

websocket_urlpatterns = [
    path('minesweeper/', consumers.MinesweeperConsumer.as_asgi()),
]
