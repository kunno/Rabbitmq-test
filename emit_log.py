#!/usr/bin/env python
import pika
import sys
import random
import time

loop_back = True
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='172.20.10.3'))
channel = connection.channel()

def start():
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
	
        channel.exchange_declare(exchange='logs',
				 type='fanout')

	message = ', '.join(str(d) for d in randPoints) or "info: Hello World!"
	channel.basic_publish(exchange='logs',
			      routing_key='',
			      body=message)
	print(" [x] Sent %r" % message)
        time.sleep(1)


    except KeyboardInterrupt:
        connection.close()

while loop_back:
    start()

