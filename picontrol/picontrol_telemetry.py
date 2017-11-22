#
#   PiControl Telemetry Process   
#   This Process forwards telemetry from any subsystem    
# 
#   Subscribes to:
#     Commands: localhost PICTL_SCHEDULER_PORT 
#     Scheduler: localhost PICTL_COMMAND_PORT 
#     cFS Manager: localhost PICTL_EXECUTIVE_PORT 
# 
#   Publishes: 
#     Telemetry: localhost TLM_UDP_PORT 
# 
# Todo: Break apart into main and helper functions.
#       Re-do the way telemetry is handled. This module has to know about
#       the format of the packet. This wont work if the number of modules expands.
#       It should just accept a generic telemetry packet with the preformatted
#       telemetry string ready to pipe out to the UDP port.
#        
#  
import sys
import zmq
import subprocess
import time
import socket
import struct

import pictl

tlm_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://localhost:' + pictl.ZMQ_SCHEDULER_PORT) # commands from scheduler
socket.connect('tcp://localhost:' + pictl.ZMQ_COMMAND_PORT)   # commands from the command app 
socket.connect('tcp://localhost:' + pictl.ZMQ_EXECUTIVE_PORT)    # tlm packets from executive
socket.connect('tcp://localhost:' + pictl.ZMQ_SENSOR_PORT)    # tlm packets from the sensor app
socket.connect('tcp://localhost:' + pictl.ZMQ_CAMERA_PORT)    # tlm packets from the camera app

#
# Setup subscription filters
#
pictl.SubscribeToFilter('SCHD002',socket)

#
#  
#
pictl.SubscribeToFilter('TELM001',socket)

while True:
   try:
      tlm_string = socket.recv()
      tlm_tokens = tlm_string.split(',')
      if tlm_tokens[0] == 'SCHD002':
          print('Received 5 sec scheduler message')
      elif tlm_tokens[0] == 'TELM001':
          print('Received Telemetry Message')
          try:
             print ('trying to send data on UDP socket')
             tlm_sock.sendto(tlm_string[8:], (pictl.UDP_TLM_IP, pictl.UDP_TLM_PORT))
          except:
                print ('Could not send packet on UDP port')
      else:
          print ('unknown telemetry packet')
           
   except KeyboardInterrupt:
      sys.exit() 

