# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
import cv2
import base64
import numpy as np

class CheckPortView(APIView):
    def get(self, request, format=None):
        return Response({'port': request.get_port()})
    
class TestPostView(APIView):
    def post(self, request, format=None):
        received_data = request.data
        return Response({'received_data': received_data})

class ProcessVideoView(APIView):
    def post(self, request, format=None):
        video_data = request.data.get('video')
        print(request.data)
        print(type(request.data))
        
        if video_data:
            # Base64로 인코딩된 영상 데이터를 디코딩하여 NumPy 배열로 변환
            video_bytes = base64.b64decode(video_data)
            video_nparray = np.frombuffer(video_bytes, dtype=np.uint8)
            video = cv2.imdecode(video_nparray, cv2.IMREAD_UNCHANGED)
            
            # 여기에서 OpenCV로 영상 처리 작업을 수행합니다.
            # 예를 들어, 영상을 회전시키는 코드
            print(video.shape)
            # rotated_video = cv2.rotate(video, cv2.ROTATE_90_CLOCKWISE)
            
            # 처리된 영상을 다시 Base64로 인코딩
            _, processed_video_bytes = cv2.imencode('.png', video)
            processed_video_data = base64.b64encode(processed_video_bytes).decode('utf-8')
            return Response({'processed_video': processed_video_data})
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