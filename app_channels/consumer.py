import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            return self.close()

        user.ws_channel_name = self.channel_name
        user.save()

        self.accept()

    def disconnect(self, close_code):
        user = self.scope["user"]

        if user.is_anonymous:
            return

        user.ws_channel_name = None
        user.last_online = timezone.now()
        user.save()

    def dispatch_named_event(self, event_name, payload):
        self.send(text_data=json.dumps({"event_name": event_name.upper(), "data": payload}))

    def prompt_create(self, event):
        self.dispatch_named_event("PROMPT_CREATE", event["data"])

    def prompt_text_receive(self, event):
        self.dispatch_named_event("PROMPT_TEXT_RECEIVE", event["data"])

    def test(self, event):
        self.dispatch_named_event("test", {})
