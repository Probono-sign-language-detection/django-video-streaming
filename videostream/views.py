# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse, HttpResponseServerError
# from django.views.decorators import gzip
from django.shortcuts import render
from rest_framework.exceptions import APIException
from django.conf import settings

import cv2
import base64
import numpy as np
from io import BytesIO
from PIL import Image
import os
# import logging
from datetime import datetime

# from time import sleep
from json import dumps
from kafka import KafkaProducer, KafkaConsumer
from json import loads



def home(request):
    return render(request, 'home.html')


class CheckPortView(APIView):
    def get(self, request, format=None):
        return Response({'port': request.get_port()})
    
    
class TestPostView(APIView):
    '''
    {"data":"test"}
    views.py 코드를 저장해야 print가 찍힌다..?
    '''
    def post(self, request, format=None):
        received_data = request.data
        print(received_data)
        # logger.debug(received_data)
        return Response({'received_data': received_data})


class VideoDecodingError(APIException):
    status_code = 400
    default_detail = 'Failed to decode video data.'
    default_code = 'video_decoding_error'


def save_decoded_image(image_data):
    now = datetime.now()
    directory = 'static/video_test'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    path = f'{directory}/image_{now.time()}.png'
    
    try:
        image = Image.open(BytesIO(image_data))
        image.save(path)
        print(f"Saved image to {path}")
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


class ProcessVideoView(APIView):
    '''
    이 API는 클라이언트로부터 영상 데이터를 받아서 
    OpenCV로 영상 처리를 수행한 후에
    base64를 kafka topic video에 전송하는 API입니다.    
    '''
    # logger = logging.getLogger(__name__)
    
    def post(self, request, format=None):
        print('request.data : ',request.data)
        
        data_dict = dict(request.data)
        
        print('data_dict : ',data_dict)
        
        en_image_data = data_dict.get('image')
        # print('image_data : ',en_image_data[:30])
        # self.logger.debug('image_data: %s', en_image_data[:30])

        if en_image_data:
            b64_image_data = base64.b64decode(en_image_data)
            print('image_data_bytes:', b64_image_data[:50])
            # logger.debug('image_data_bytes: %s', b64_image_data[:50])
            # remove the header from the base64 string
            bin_image_data = base64.b64decode(b64_image_data)
            print('image_data_bytes:', bin_image_data[:50])
            # logger.debug('image_data_bytes: %s', bin_image_data[:50])
            
            # save the image data as an image
            flag = save_decoded_image(bin_image_data)
            if flag:
                print('saved image')
                # self.logger.debug('saved image')
                
            producer = KafkaProducer(
                bootstrap_servers=['kafka:19092'],
                value_serializer=lambda x: dumps(x).encode('utf-8')
            )    
            
            data = {'image': en_image_data}
            
            # topic video에 데이터 전송 
            producer.send('video', value=data)
            producer.flush()
            
            print('sent data to kafka')
                
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




## local video streaming
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



def detectme(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print('에러 발생:', str(e))
        return HttpResponseServerError('Internal Server Error')
    
    
    
