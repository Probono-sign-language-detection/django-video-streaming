import cv2
import json

import numpy as np
import base64
from channels.generic.websocket import AsyncWebsocketConsumer


from kafka import KafkaConsumer
from json import loads
from channels.consumer import SyncConsumer


class KafkaVideoConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.consumer = KafkaConsumer(
            'video',
            bootstrap_servers=['kafka:19092'],
            auto_offset_reset='latest',
            enable_auto_commit=True,
            # group_id='my-group-id',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )

    def kafka_video_consumer(self, event):
        for kafka_event in self.consumer:
            event_data = kafka_event.value
            # Do whatever you want
            print(event_data['image'][:30])
            # sleep(1)


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        # response to client, that we are connected.
        await self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Connected"
            }
        }))

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