#
# ZMQ REP Server for the Pimoroni Enviro PHAT for the Raspberry Pi
# Binds REP socket to tcp://*:5555
#
import time
import sys
import zmq

# Pimoroni enviro pHat support
import enviro_phat_server

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
   try:
      #  Wait for next request from client
      message = socket.recv()

      # Depending on the ID, pass it to the needed sensor function
      message_list = message.split(',')   

      # This is where the right server function is called 
      if message_list[1] == 'DEV=ENVIRO_PHAT':
         message = enviro_phat_server.process_sensor_req(message)
      else:
         # unknown message
         message = "SENSOR_REP," + message_list[1] + ",ERROR=UNKNOWN_ID,SENSOR_REP_END"

      #  Send reply back to client
      socket.send(message)
   except KeyboardInterrupt:    
      sys.exit()
