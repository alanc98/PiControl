#
# ZMQ REP Server for the Raspberry Pi Camera
# Binds REP socket to tcp://*:5557
#
import time
import sys
import zmq

# Raspberry pi camera support
import pi_camera_server

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5557")

while True:
   try:
      #  Wait for next request from client
      message = socket.recv()

      # Depending on the ID, pass it to the needed sensor function
      message_list = message.split(',')   

      if message_list[1] == 'DEV=PI_CAMERA':
         message = pi_camera_server.process_sensor_req(message)
      else:
         # unknown message
         message = "SENSOR_REP," + message_list[1] + ",ERROR=UNKNOWN_ID,SENSOR_REP_END"

      #  Send reply back to client
      socket.send(message)
   except KeyboardInterrupt:    
      sys.exit()
