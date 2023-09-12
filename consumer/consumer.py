from kafka import KafkaConsumer
from json import loads
from time import sleep
# import daemon
# from dotenv import load_dotenv
import os

from datetime import datetime
import requests
import json

# Load the environment variables from the .env file
# load_dotenv()
## model class

## feature class
class Consumer:
    def __init__(self, brokers, topicName):
        self.consumer = KafkaConsumer(
            topicName,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id="video-consumer-group",
            bootstrap_servers=brokers,
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
    
    def consume(self):
        file_path = './kafka-output.txt'
        if os.path.exists(file_path):
            os.remove(file_path)

        # micro 배치 처리 
        # -> 몇 장 : 100 frame -> 1 batch
        # 10초
        
        with open(file_path, 'a') as file:
            word_list = []
            for event in self.consumer:
                now = datetime.now()
                now_time = now.strftime('%Y-%m-%d %H:%M:%S')
                
                event_data = event.value
                # Write event_data['image'][:30] to the text file
                session_id = event_data['session_id']
                id = event_data['id']
                word = event_data['word']
                
                image = event_data['image'][:10]
                
                file.write(f'{now_time}, {session_id} : {image} \n')
                print(f'{now_time}, {session_id} : {image}')
                # Flush the buffer to ensure immediate write
                file.flush()
                
                
                response = requests.post(
                    'http://django:8000/video/sessiondata-save/',  
                    data=json.dumps({
                        'session_id': session_id,
                        'id': id,
                        'word': word
                    }),
                    headers={'Content-Type': 'application/json'}
                )
                
                print('database save :', response)
                # print(response.json())
                
                sleep(1)


if __name__ == '__main__':
    topicName = 'video'
    brokers = ['kafka:19092']
    consumer = Consumer(brokers, topicName)
    while True:
        consumer.consume()



