from __future__ import print_function
import zmq,time,sys
 
print("Connecting to Sensor Server")
sys.stdout.flush()
context = zmq.Context()
#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")
print("Connected")

print("Sending BMP sub start")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=BMP,CMD=SUB_START,RATE=1000,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

print("Sending LUX sub start")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=LUX,CMD=SUB_START,RATE=1000,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

print("Sending MAG sub start")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=MAG,CMD=SUB_START,RATE=1000,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

print("Sending ACCEL sub start")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=ACCEL,CMD=SUB_START,RATE=1000,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

print("Sending HEADING sub start")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=HEADING,CMD=SUB_START,RATE=1000,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

print("Sending ANALOG sub start")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=ANALOG,CMD=SUB_START,RATE=1000,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

print("Wait for 1 minute...check the sub reader")
time.sleep(60)

print("Sending BMP sub stop")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=BMP,CMD=SUB_STOP,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

print("Sending LUX sub stop")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=LUX,CMD=SUB_STOP,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

print("Sending MAG sub stop")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=MAG,CMD=SUB_STOP,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

print("Sending ACCEL sub stop")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=ACCEL,CMD=SUB_STOP,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

print("Sending HEADING sub stop")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=HEADING,CMD=SUB_STOP,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

print("Sending ANALOG sub stop")
socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=ANALOG,CMD=SUB_STOP,SENSOR_REQ_END")
message = socket.recv()
print("Received:",message)

