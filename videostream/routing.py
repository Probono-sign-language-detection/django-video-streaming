from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/video_rtc/', consumers.VideoConsumer.as_asgi()),
]