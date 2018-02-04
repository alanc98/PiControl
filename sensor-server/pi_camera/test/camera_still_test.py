from __future__ import print_function
import zmq,time,sys
 
print("Connecting to Sensor Server")
sys.stdout.flush()
context = zmq.Context()
#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5557")
print("Connected")

socket.send("SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=STILL,CMD=CAPTURE,SIZE=2,VFLIP=TRUE,FILE=/home/pi/Desktop/test.jpg,SENSOR_REQ_END")
message = socket.recv()
print("Received Pi_Camera sensor reply:",message)
time.sleep(5)
socket.send("SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=STILL,CMD=CAPTURE,SIZE=3,VFLIP=FALSE,FILE=/home/pi/Desktop/test2.jpg,SENSOR_REQ_END")
message = socket.recv()
print("Received Pi_Camera sensor reply:",message)
