import json

from channels.generic.websocket import AsyncWebsocketConsumer


class SomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_code"]
        self.room_group_name = "room_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )  # noqa: E501
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )  # noqa: E501

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.send(text_data=json.dumps({"message": message}))
