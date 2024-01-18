import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ProbeData, Probe
import datetime

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
        self.probe = None
        self.probe_id = self.scope["url_route"]["kwargs"]["probe_id"]
        try:
            if not Probe.objects.filter(probe_id=self.probe_id).exists():
                self.room_group_name = "probe_%s" % self.probe_id
                self.close()
                return
        except:
            self.room_group_name = "probe_%s" % self.probe_id
            self.close()
            return
        self.probe = Probe.objects.get(probe_id=self.probe_id)
        self.probe.active = True
        self.probe.save()
        self.room_group_name = "probe_%s" % self.probe_id
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        if self.probe:
            self.probe.active = False
            self.probe.save()
        async_to_sync(
            self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )
        )

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            print(text_data_json)
        except json.decoder.JSONDecodeError:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "error",
                    "code": JSON_DECODE_ERROR,
                    "error": ERROR_MESSAGES[JSON_DECODE_ERROR],
                },
            )
            return
        if not check_data(text_data_json):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "error",
                    "code": DATA_NOT_VALID,
                    "error": ERROR_MESSAGES[DATA_NOT_VALID],
                },
            )
            return
        probe_data = ProbeData(
            probe_id=self.probe_id,
            temperature=text_data_json["temperature"],
            humidity=text_data_json["humidity"],
            soil_moisture=text_data_json["soil_moisture"],
            light_level=text_data_json["light_level"],
            read_time=datetime.datetime.now(),
        )
        probe_data.save()
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


def check_data(data):
    try:
        if (
            data["temperature"] == None
            or data["humidity"] == None
            or data["soil_moisture"] == None
            or data["light_level"] == None
        ):
            return False
        if float(data["temperature"]) > 100 or float(data["temperature"]) < -100:
            return False
        if float(data["humidity"]) > 100 or float(data["humidity"]) < 0:
            return False
        if float(data["soil_moisture"]) > 100 or float(data["soil_moisture"]) < 0:
            return False
        if float(data["light_level"]) > 100 or float(data["light_level"]) < 0:
            return False
    except:
        return False
    return True
