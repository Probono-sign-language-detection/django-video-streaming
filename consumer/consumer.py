from kafka import KafkaConsumer
from json import loads
from time import sleep
# import daemon
import os


def run_consumer():
    consumer = KafkaConsumer(
        'video',
        bootstrap_servers=['kafka:19092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        # group_id='my-group-id',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    file_path = './kafka-output.txt'
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'a') as file:
        for event in consumer:
            event_data = event.value
            # Write event_data['image'][:30] to the text file
            file.write(event_data['image'][:30] + '\n')
            print(event_data['image'][:30])
            # Flush the buffer to ensure immediate write
            file.flush()
            # sleep(1)



if __name__ == '__main__':
    run_consumer()

# with daemon.DaemonContext():
#     run_consumer()