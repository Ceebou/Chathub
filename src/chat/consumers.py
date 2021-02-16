from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from datetime import datetime
import pytz

ROOM_NAME = "defaultRoom"
GROUP_NAME = "defaultGroup"


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.room_name = ROOM_NAME
        self.room_group_name = "chat_%s" % self.room_name
        # Join channel
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive new message from user
    def receive(self, text_data=None):
        textDataJson = json.loads(text_data)
        print(self.user)
        username = str(self.user)
        print(type(username))
        print(username)
        message = {
            "text": textDataJson["message"],
            "author": username,
            "timestamp": self.getTimeStamp()
        }
        print("got from user")
        print(textDataJson)
        # Send message to other users
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chatMessage",
                "senderChannelName": self.channel_name,
                "message": message
            }
        )
        message["author"] = "Me"
        self.send(text_data=json.dumps({"message": message}))

    # Receive new message from different user and send to self
    def chatMessage(self, event):
        if self.channel_name == event["senderChannelName"]:
            return
        message = event["message"]
        print("got message from room")
        print(message)
        self.send(text_data=json.dumps({"message": message}))

    def getTimeStamp(self):
        utcNow = datetime.now()
        utc1 = utcNow.astimezone(pytz.timezone("Etc/GMT-1"))
        return utc1.strftime("%H:%M %d.%m")
