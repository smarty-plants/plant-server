import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import server.routing


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plantserver.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(server.routing.websocket_urlpatterns)
        ),
    }
)
