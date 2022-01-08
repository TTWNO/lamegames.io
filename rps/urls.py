from django.urls import path
from . import views

urlpatterns = [
    path('rps/', views.rps, name="rps"),
    path('rps/select', views.rps_select, name="rps/select"),
    path('rps/create', views.rps_create, name="rps/create"),
    path('rps/join/<room_id>', views.rps_join, name='rps/join'),
    path('minesweeper/', views.minesweeper, name='minesweeper')
]