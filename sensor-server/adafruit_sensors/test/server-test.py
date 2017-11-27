from __future__ import print_function
import zmq,time,sys
 
print("Connecting to Sensor Server")
sys.stdout.flush()
context = zmq.Context()
#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")
print("Connected")
while(True):
    socket.send("SENSOR_REQ,DEV=ADA_BMP180,SUB_DEV=BMP,CMD=READ,SENSOR_REQ_END")
    message = socket.recv()
    print("Received BMP Data:",message)
    # time.sleep(1)
    socket.send("SENSOR_REQ,DEV=ADA_TSL2561,SUB_DEV=LUX,CMD=READ,SENSOR_REQ_END")
    message = socket.recv()
    print("Received LUX Data:",message)
    # time.sleep(1)
