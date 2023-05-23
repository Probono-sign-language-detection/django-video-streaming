import cv2
import numpy as np
import base64
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # 전송된 데이터 처리
        # text_data에는 React Native에서 보낸 Base64 인코딩된 이미지 데이터가 포함됩니다.
        # 예시에서는 OpenCV를 사용하여 이미지 디코딩 후 처리하는 과정을 보여줍니다.

        # Base64 디코딩
        img_data = base64.b64decode(text_data)

        # 이미지 데이터를 numpy 배열로 변환
        nparr = np.frombuffer(img_data, dtype=np.uint8)

        # numpy 배열을 OpenCV 이미지로 변환
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 이미지 처리 로직 수행
        # 예를 들어, 이미지를 저장하거나 얼굴 인식 등의 작업을 수행할 수 있습니다.

        # 처리된 이미지를 다시 Base64 인코딩
        _, img_encoded = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')

        # 처리된 이미지 데이터를 클라이언트로 전송
        await self.send(img_base64)