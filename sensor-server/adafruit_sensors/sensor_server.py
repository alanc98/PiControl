#
# ZMQ REP Server for  
# Binds REP socket to tcp://*:5556
#
import time
import zmq

# LUX sensor
import tsl_lux_server 

# BMP180  sensors
import bmp180_server 

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

while True:
    #  Wait for next request from client
    message = socket.recv()

    # Depending on the ID, pass it to the right sensor function
    message_list = message.split(',')   

    # This is where the right server function is called 
    if message_list[1] == 'DEV=ADA_TSL2561':
       message = tsl_lux_server.process_req(message)
    elif message_list[1] == 'DEV=ADA_BMP180':
       message = bmp180_server.process_req(message)
    else:
       # unknown message
       message = "SENSOR_REP," + message_list[1] + ",ERROR=UNKNOWN_ID,SENSOR_REP_END"

    #  Send reply back to client
    socket.send(message)

