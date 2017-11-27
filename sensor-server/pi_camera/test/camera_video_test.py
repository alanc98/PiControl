from __future__ import print_function
import zmq,time,sys
 
print("Connecting to Sensor Server")
sys.stdout.flush()
context = zmq.Context()
#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5557")
print("Connected")

socket.send("SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=VIDEO,CMD=CAPTURE,SIZE=2,VFLIP=TRUE,DURATION=10,FILE=/home/pi/Desktop/testvid.h264,SENSOR_REQ_END")
message = socket.recv()
print("Received Pi_Camera sensor reply:",message)
