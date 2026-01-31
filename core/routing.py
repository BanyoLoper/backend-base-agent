from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Por ahora el router de mensajes está vacío, lo llenaremos al crear la App de agentes
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Aquí irán las rutas de tus websockets
        ])
    ),
})