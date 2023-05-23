from django.urls import include, path
from rest_framework import routers
from .views import *

urlpatterns = [
    # 다른 URL 패턴들...
    path('check-port/', CheckPortView.as_view(), name='check_port'),

    path('process-video/', ProcessVideoView.as_view(), name='process_video'),
    path('process-upload-video/', ProcessUploadVideoView.as_view(), name='process_upload_video'),
    path('test-post/', TestPostView.as_view(), name='test_post'),

]