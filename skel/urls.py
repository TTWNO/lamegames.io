from django.urls import path, include

from . import views
from . import consumers

urlpatterns = [
    # /skel/ sends to the index page (see views.py to see what index does...
    # make sure name="skel" matches the name in lamegames/settings.py
    path("", views.index, name="skel"),
]

websocket_urlpatterns = [
    # any websocket connection attempting connection at /skel/ will be dealt with by the SkelConsumer object; see more info in consumers.py
    path("skel/", consumers.SkelConsumer.as_asgi()),
]
