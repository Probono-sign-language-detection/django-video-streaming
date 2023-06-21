# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
import cv2
import base64
import numpy as np
from django.http import StreamingHttpResponse, HttpResponseServerError
import threading
from django.views.decorators import gzip
from django.shortcuts import render
from rest_framework.exceptions import APIException
import io
from io import BytesIO
from PIL import Image
import re
from django.core.files.base import ContentFile
import os
from django.conf import settings


class CheckPortView(APIView):
    def get(self, request, format=None):
        return Response({'port': request.get_port()})
    
class TestPostView(APIView):
    def post(self, request, format=None):
        received_data = request.data
        return Response({'received_data': received_data})


class VideoDecodingError(APIException):
    status_code = 400
    default_detail = 'Failed to decode video data.'
    default_code = 'video_decoding_error'


def save_decoded_image(image_data, path='static/video_test/image.png'):
    try:
        # with open('static/video_test/image.png', 'wb') as f:
        #     f.write(image_data)
        image = Image.open(BytesIO(image_data))
        image.save(path)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


class ProcessVideoView(APIView):
    def post(self, request, format=None):
        en_image_data = request.data.get('image')
        print('image_data : ',en_image_data[:30])
        # print(type(request.data))
        # en_image_data = re.sub('^data:image/.+;base64,', '', en_image_data)
        # print('video_data : ',en_image_data[:30])
        if en_image_data:
            b64_image_data = base64.b64decode(en_image_data)
            print('image_data_bytes:', b64_image_data[:50])
            # remove the header from the base64 string
            bin_image_data = base64.b64decode(b64_image_data)
            print('image_data_bytes:', bin_image_data[:50])
            # save the image data as an image
            flag = save_decoded_image(bin_image_data)
            if flag:
                print('saved image')
            return Response({'message': 'Image saved successfully'})
        else:
            return Response({'error': 'No video data received'}, status=400)
   
        

class ProcessUploadVideoView(APIView):
    def post(self, request, format=None):
        # 디버깅 코드: 데이터 타입 출력
        print(type(request.data))
    
        video_file = request.FILES.get('video')
        
        if video_file:
            video_bytes = video_file.read()  # 파일 읽기
            video_nparray = np.frombuffer(video_bytes, dtype=np.uint8)
            video = cv2.imdecode(video_nparray, cv2.IMREAD_UNCHANGED)
            
            # 여기에서 OpenCV로 영상 처리 작업을 수행합니다.
            # 예를 들어, 영상을 회전시키는 코드
            print(video.shape)
            # rotated_video = cv2.rotate(video, cv2.ROTATE_90_CLOCKWISE)
            _, processed_video_bytes = cv2.imencode('.png', video)
            processed_video_data = base64.b64encode(processed_video_bytes).decode('utf-8')
            return Response({'processed_video': processed_video_data})
        else:
            return Response({'error': 'No video file received'}, status=400)




class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        if ret:
            _, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        else:
            print("Failed to capture frame")
            return None


def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def home(request):
    return render(request, 'home.html')


def detectme(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print('에러 발생:', str(e))
        return HttpResponseServerError('Internal Server Error')