#
#   PiControl Pi Camera Process   
#   This Process sends commands to the sensor server to control the Raspberry Pi Camera 
# 
#   Subscribes to:
#     Commands: localhost  ZMQ_COMMAND_PORT 
#     Scheduler: localhost ZMQ_SCHEDULER_PORT 
# 
#   Publishes: 
#     Telemetry: localhost ZMQ_SENSOR_PORT  
# 
#   Uses REQ/REP Socket: ZMQ_SENSOR_SERVER_PORT
#
# Todo: Break apart into main and helper functions
#       Preferably break this apart into a class with global variables in the class
#  
import sys
import zmq
import time
import struct 

import pictl

#
# Globals for telemetry
#

# process number
global proc

# Global - Command counter
camera_cmd_counter = 0

# Global - Command error counter
camera_err_counter = 0

# Global - camera status
camera_status = 0

# Global ZeroMQ context
context = zmq.Context()

# Command Socket 
sub_socket = context.socket(zmq.SUB)
sub_socket.connect('tcp://localhost:' + pictl.ZMQ_SCHEDULER_PORT)
sub_socket.connect('tcp://localhost:' + pictl.ZMQ_COMMAND_PORT)

# Telemety Socket  
pub_socket = context.socket(zmq.PUB)
pub_socket.bind('tcp://*:' + pictl.ZMQ_SENSOR_PORT)

# Sensor server Socket
sens_srv_socket = context.socket(zmq.REQ)
sens_srv_socket.connect('tcp://localhost:' + pictl.ZMQ_SENSOR_SERVER_PORT)

#
# Setup subscription filters
#
pictl.SubscribeToFilter('SCHD002',sub_socket)
pictl.SubscribeToFilter('PCAM001',sub_socket)

#
# Accept commands to capture pictures, videos, or timelapse sequences
#

while True:
   try:
      string = sub_socket.recv_string()
      string = string.decode('ascii')
      cmd_tokens = string.split(',')
      print(string)
      if cmd_tokens[0] == 'SCHD002':
          #
          # Send command counters and LED status
          #
          tlm_packet = struct.pack('8shhhh','TELM001,',0x100A, camera_cmd_counter, camera_err_counter , camera_status)
          pub_socket.send(tlm_packet)
          
      # elif cmd_tokens[0] == 'SCHD001':
      #     print('1hz scheduler message')
      elif cmd_tokens[0] == 'PCAM001':

          if cmd_tokens[1] == 'NOOP':
              print('Received PiCam command - NOOP')
              camera_cmd_counter += 1

          if cmd_tokens[1] == 'CAPTURE_IMAGE':
              print('Received PICAM command - CAPTURE_IMAGE')
              camera_cmd_counter += 1
              #
              # Send the CAPTURE_IMAGE command
              #
              #sens_srv_socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=LED,CMD=LED_ON,SENSOR_REQ_END")
              #sensor_message = sens_srv_socket.recv()

          elif cmd_tokens[1] == 'CAPTURE_VIDEO':
             print('Received PICAM command - CAPTURE_VIDEO')
             camera_cmd_counter += 1
             #
             # Send the CAPTURE command
             #
             # sens_srv_socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=LED,CMD=LED_OFF,SENSOR_REQ_END")
             # sensor_message = sens_srv_socket.recv()

   except KeyboardInterrupt:
      sys.exit() 
