from django.urls import include, path
from rest_framework import routers
from .views import *

urlpatterns = [
    # 다른 URL 패턴들...
    path('process-video/', ProcessVideoView.as_view(), name='process_video'),
    
    path('test-post/', TestPostView.as_view(), name='test_post'),

]