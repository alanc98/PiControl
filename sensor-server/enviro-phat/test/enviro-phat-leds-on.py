from __future__ import print_function
import zmq,time,sys
 
print("Connecting to Sensor Server")
sys.stdout.flush()
context = zmq.Context()
#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")
print("Connected")

socket.send("SENSOR_REQ,DEV=EPH_LED,CMD=LED_ON,SENSOR_REQ_END")
message = socket.recv()
print("Received Enviro Phat LED Data:",message)