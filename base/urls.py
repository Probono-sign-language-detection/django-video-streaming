from django.urls import path
from .views import *

urlpatterns = [
    path('', check_connection, name='check-connection'),
    # 다른 URL 패턴들을 여기에 추가할 수 있습니다.
]