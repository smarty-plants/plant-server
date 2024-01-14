from django.urls import path
from . import views

urlpatterns = [
    path("websocket/", views.websocket_view),
    path("plants/", views.PlantApiView.as_view()),
    path("probes/daily/", views.ProbeDailyApiView.as_view()),
    path("probes/current/", views.ProbeCurrentReadingsApiView.as_view()),
]
