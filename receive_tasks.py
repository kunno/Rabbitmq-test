#! /usr/bin/eny python
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='172.31.98.95'))
channel = connection.channel()
second_channel = connection.channel()
third_channel = connection.channel()
fourth_channel = connection.channel()

channel.queue_declare(queue='receive_tasks', durable=True)
second_channel.queue_declare(queue='logs', durable=True)
third_channel.queue_declare(queue='gps_feed', durable=True)
fourth_channel.queue_declare(queue='usb_feed', durable=True)



print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received [%r]" % body)
   # time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
second_channel.basic_qos(prefetch_count=1)
third_channel.basic_qos(prefetch_count=1)
fourth_channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback, queue='receive_tasks')
second_channel.basic_consume(callback, queue='logs')
third_channel.basic_consume(callback, queue='gps_feed')
fourth_channel.basic_consume(callback, queue='usb_feed')


channel.start_consuming()
second_channel.start_consuming()
thrid_channel.start_consuming()
fourth_channel.start_consuming()
