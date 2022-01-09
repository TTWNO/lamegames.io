from channels.generic.websocket import WebsocketConsumer
from common.models import LameUser

class SkelConsumer(WebsocketConsumer):
    # the first time any user attempts connection to this websocket
    def connect(self):
        # accept and activate connection
        self.accept()
        # get user from information passed to us via middleware (aka scope)
        self.user = LameUser.objects.get(username=self.scope['user'].username)

    # sometimes we need to send additional information when a client disconnects, but in the trivial case we can leave it blank like so
    def disconnect(self, close_code):
        pass

    # When ANY message is received
    def receive(self, text_data):
        # Send message to client
        self.send("Hello, " + self.user.username + "; this is from the websocket!")
