#!/usr/bin/env python
import pika
import sys
import time
import random
import socket
import serial

loop_back = False
connected = False

def start():
    try:

        x = random.randint(2, 1000)

        multiples = []
        results = []
        for i in xrange(2, x+1):
            if i not in multiples:
                results.append(i)
                for j in xrange(i*i, x+1, i):
                    multiples.append(j)
                

        channel.queue_declare(queue='receive_tasks', durable=True)

        message = ', '.join(str(d) for d in results) or "info: Hello World!"

        channel.basic_publish(exchange='', routing_key='receive_tasks',
                body=message, properties=pika.BasicProperties(
                    delivery_mode = 2, ))

        print(" [x] Sent [%r]" % message)
        #time.sleep(5)

    except KeyboardInterrupt:
        connection.close()

def second_start():
    try:
	radius = 200
	rangeX = (0, 2500)
	rangeY = (0, 2500)
	qty = 10

	deltas = set()
	for x in range(-radius, radius+1):
	    for y in range(-radius, radius+1):
		if x*x + y*y <= radius*radius:
		    deltas.add((x,y))

	randPoints = []
	excluded = set()
	i = 0
	while i < qty:
	    x = random.randrange(*rangeX)
	    y = random.randrange(*rangeY)
	    if (x,y) in excluded: continue
	    randPoints.append((x,y))
	    i += 1
	    excluded.update((x+dx, y+dy) for (dx, dy) in deltas)
	
        second_channel.queue_declare(queue='logs', durable=True)

	message = ', '.join(str(d) for d in randPoints) or "info: Hello World!"
	second_channel.basic_publish(exchange='',
			      routing_key='logs',
			      body=message, properties=pika.BasicProperties(
                                  delivery_mode=2 ))
	print(" [x] Sent %r" % message)
        #time.sleep(1)


    except KeyboardInterrupt:
        connection.close()

def nc_start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.41.31', 51112))
        while 1:
            data = ""
            while not data.endswith("\r\n"):
               data+= s.recv(3)

            third_channel.queue_declare(queue='gps_feed', durable=True)
            third_channel.basic_publish(exchange='',
                    routing_key='gps_feed', body=data,
                    properties=pika.BasicProperties(
                        delivery_mode=2 ))
            print(" [x] Sent %r" % data)
    except KeyboardInterrupt:
        s.close()
        connection.close()

def usb_start():
    try:
        ser = serial.Serial('/dev/ttyUSB0', 19200, timeout = 5)

        while 1:
            data = ser.readline()
            fourth_channel.queue_declare(queue='usb_feed', durable=True)
            fourth_channel.basic_publish(exchange='',
                    routing_key='usb_feed', body=data,
                    properties=pika.BasicProperties(
                        delivery_mode=2 ))
            print(" [x] Sent %r" % data)

    except KeyboardInterrupt:
        sys.exit()
        connection.close()

while connected == False:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host ='137.110.151.102'))
        channel = connection.channel()
        second_channel = connection.channel()
        third_channel = connection.channel()
        fourth_channel = connection.channel()
        connected = True
        loop_back = True
        while loop_back == True:
            try:
                #nc_start()
                #usb_start()
                start()
                second_start()
            except pika.exceptions.ConnectionClosed:
                loop_back = False
                connected = False
                time.sleep(5)
                continue
            except KeyboardInterrupt:
                loop_back = False
                Connected = False
                sys.exit()
                connection.close()
                break

    except pika.exceptions.ConnectionClosed:
        loop_back = False
        connected = False
        time.sleep(5)
        continue
    except KeyboardInterrupt:
        loop_back = False
        Connected = False
        sys.exit()
        connection.close()
        break

