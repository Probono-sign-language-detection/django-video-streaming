from kafka import KafkaConsumer
from json import loads
from time import sleep
# import daemon
import os
from datetime import datetime


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

        with open(file_path, 'a') as file:
            for event in self.consumer:
                now = datetime.now()
                now_time = now.strftime('%Y-%m-%d %H:%M:%S')
                
                event_data = event.value
                # Write event_data['image'][:30] to the text file
                data = event_data['image'][:30]
                file.write(f'{now_time} : {data} \n')
                print(f'{now_time} : {data}')
                # Flush the buffer to ensure immediate write
                file.flush()
                sleep(1)


if __name__ == '__main__':
    topicName = 'video'
    brokers = ['kafka:19092']
    consumer = Consumer(brokers, topicName)
    while True:
        consumer.consume()





# def run_consumer():
#     consumer = KafkaConsumer(
#         'video',
#         bootstrap_servers=['kafka:19092'],
#         auto_offset_reset='earliest',
#         enable_auto_commit=True,
#         # group_id='my-group-id',
#         value_deserializer=lambda x: loads(x.decode('utf-8'))
#     )

#     file_path = './kafka-output.txt'
#     if os.path.exists(file_path):
#         os.remove(file_path)

#     with open(file_path, 'a') as file:
#         for event in consumer:
#             event_data = event.value
#             # Write event_data['image'][:30] to the text file
#             file.write(event_data['image'][:30] + '\n')
#             print(event_data['image'][:30])
#             # Flush the buffer to ensure immediate write
#             file.flush()
#             # sleep(1)


# with daemon.DaemonContext():
#     run_consumer()