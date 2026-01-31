import os
import django
from django.core.asgi import get_asgi_application

# 1. Definir la configuración de Django (Debe ser lo PRIMERO)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 2. Inicializar Django manualmente para asegurar que todas las apps (como 'channels') estén listas
django.setup()

# 3. Crear la aplicación HTTP de Django
django_asgi_app = get_asgi_application()

# 4. AHORA Y SOLO AHORA, podemos importar los ruteos de nuestra app
# Esto evita el error de DEFAULT_CHANNEL_LAYER
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import agents.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            agents.routing.websocket_urlpatterns
        )
    ),
})