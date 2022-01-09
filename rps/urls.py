from django.urls import path
from . import views
from . import consumers

urlpatterns = [
    path('rps/', views.rps, name="rps"),
    path('rps/select', views.rps_select, name="rps/select"),
    path('rps/create', views.rps_create, name="rps/create"),
    path('rps/join/<room_id>', views.rps_join, name='rps/join'),
]

websocket_urlpatterns = [
    path("rps/<id>", consumers.RPSConsumer.as_asgi()),
]
