from __future__ import print_function
import zmq,time,sys
 
print("Connecting to Sensor Server")
sys.stdout.flush()
context = zmq.Context()
#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")
print("Connected")

led_on = 0

while(True):
    socket.send("SENSOR_REQ,DEV=EPH_BMP,CMD=READ,SENSOR_REQ_END")
    message = socket.recv()
    print("Received Enviro Phat BMP Data:",message)

    socket.send("SENSOR_REQ,DEV=EPH_LIGHT,CMD=READ,SENSOR_REQ_END")
    message = socket.recv()
    print("Received Enviro Phat LIGHT Data:",message)

    socket.send("SENSOR_REQ,DEV=EPH_ACCEL,CMD=READ,SENSOR_REQ_END")
    message = socket.recv()
    print("Received Enviro Phat ACCEL Data:",message)

    socket.send("SENSOR_REQ,DEV=EPH_HEADING,CMD=READ,SENSOR_REQ_END")
    message = socket.recv()
    print("Received Enviro Phat HEADING Data:",message)

    socket.send("SENSOR_REQ,DEV=EPH_MAG,CMD=READ,SENSOR_REQ_END")
    message = socket.recv()
    print("Received Enviro Phat MAG Data:",message)

    if led_on == 0:
       socket.send("SENSOR_REQ,DEV=EPH_LED,CMD=LED_ON,SENSOR_REQ_END")
       message = socket.recv()
       print("Received Enviro Phat LED Data:",message)
       led_on = 1 
    else:
       socket.send("SENSOR_REQ,DEV=EPH_LED,CMD=LED_OFF,SENSOR_REQ_END")
       message = socket.recv()
       print("Received Enviro Phat LED Data:",message)
       led_on = 0

    print('..')

    time.sleep(1)


