from django.urls import path
from . import views

urlpatterns = [
    # path("websocket/", views.websocket_view, name="websocket"),
    path("", views.CheckApi.as_view()),
    path("plants/", views.PlantApiView.as_view()),
    path("probes/daily/", views.ProbeDailyApiView.as_view()),
    path("probes/current/", views.ProbeCurrentReadingsApiView.as_view()),
    path("probes/details/<slug:probe_id>/", views.ProbeDetailApiView.as_view()),
    path("probes/add/", views.ProbeCreateView.as_view()),
    path("plants/add/", views.PlantCreateView.as_view()),
    path("probe/create/", views.CreateProbeApi.as_view()),
    path("probe/check/", views.CheckProbeApi.as_view()),
    path("probe/detail/<slug:probe_id>/", views.ProbeDetailApi.as_view()),
]
