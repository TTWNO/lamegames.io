"""lamegames URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings

import chat, rps, minesweeper
from chat import consumers
from rps import consumers
from minesweeper import consumers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    #path('chat/', include('chat.urls')),
    #path('games/', include('games.urls')),
    #path('chess/', include('chess.urls'))
    *[path(game["url"] + "/", include(game["urls"])) for game in settings.VISIBLE_GAME_LINKS]
]

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', chat.consumers.ChatConsumer.as_asgi()),
    path('rps/<id>', rps.consumers.RPSConsumer.as_asgi()),
    path('minesweeper/', minesweeper.consumers.MinesweeperConsumer.as_asgi())
]
