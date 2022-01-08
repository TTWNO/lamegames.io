from django.urls import path
from . import views

urlpatterns = [
    path('minesweeper/', views.minesweeper, name='minesweeper')
]
