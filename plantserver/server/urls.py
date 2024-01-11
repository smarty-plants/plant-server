from django.urls import path
from . import views

urlpatterns = [
    path("websocket/", views.websocket_view),
]
