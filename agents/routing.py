from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/realm/', consumers.RealmConsumer.as_asgi()),
]