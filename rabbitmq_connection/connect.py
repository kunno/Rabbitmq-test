import header
import pika

def start_connect():
    try:
        print(" [x] Establishing connection...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = header.host_address))
        channel = connection.channel()
        channel.queue_declare(queue=header.host_queue,
                duarble=header.queue_duration)
        print(" [x] Connection established!")
    except pika.exceptions.ConnectionClosed:
        connection.close()
