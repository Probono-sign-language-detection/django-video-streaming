from django.urls import include, path
from rest_framework import routers
from .views import *
from . import views

urlpatterns = [
    # 다른 URL 패턴들...
    path('check-port/', CheckPortView.as_view(), name='check_port'),

    # process-video - video encoding
    path('process-video/', ProcessVideoView.as_view(), name='process_video'),
    
    path('sessiondata-save/', SessionDataSaveView.as_view(), name='sessiondata_save'),
    
    # path('process-upload-video/', ProcessUploadVideoView.as_view(), name='process_upload_video'),
    
    path('test-post/', TestPostView.as_view(), name='test_post'),

    path('', views.home,name="home"), # 웹사이트 링크 home.html
    path("detectme", views.detectme,name="detectme"), # 웹캠 링크
    
]