from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/probe/<slug:probe_id>/", consumers.ProbeConsumer.as_asgi()),
]
