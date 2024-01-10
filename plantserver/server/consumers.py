import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

DATA_APPROVED = 1
JSON_DECODE_ERROR = 2
DATA_NOT_VALID = 3

ERROR_MESSAGES = {
    DATA_APPROVED: "Data approved",
    JSON_DECODE_ERROR: "JSON decode error",
    DATA_NOT_VALID: "Data not valid",
}


class ProbeConsumer(WebsocketConsumer):
    def connect(self):
        self.probe_id = self.scope["url_route"]["kwargs"]["probe_id"]
        self.room_group_name = "probe_%s" % self.probe_id
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(
            self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )
        )

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.decoder.JSONDecodeError:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "error",
                    "code": JSON_DECODE_ERROR,
                    "message": ERROR_MESSAGES[JSON_DECODE_ERROR],
                },
            )
        # TODO validate probe data
        if False:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "error",
                    "code": DATA_NOT_VALID,
                    "message": ERROR_MESSAGES[DATA_NOT_VALID],
                },
            )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "probe_data_approved",
                "message": ERROR_MESSAGES[DATA_APPROVED],
                "code": DATA_APPROVED,
            },
        )

    def error(self, event):
        print(event)
        message = event["error"]
        self.send(text_data=json.dumps({"error": message}))

    def probe_data_approved(self, event):
        print(event)
        message = event["message"]
        self.send(text_data=json.dumps(message))
