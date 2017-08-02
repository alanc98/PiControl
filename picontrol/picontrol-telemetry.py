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

fifthhz_filter = "SCHD002"
if isinstance(fifthhz_filter, bytes):
    fifthhz_filter = fifthhz_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, fifthhz_filter)

# Setup filter for telemetry packets
tlm_filter = "TELM001"
if isinstance(tlm_filter, bytes):
    tlm_filter = tlm_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, tlm_filter)

# Setup filter for Sensor telemetry packets
tlm_filter2 = "TELM002"
if isinstance(tlm_filter2, bytes):
    tlm_filter2 = tlm_filter2.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, tlm_filter2)

while True:
   try:
      string = socket.recv_string()
      string = string.decode('ascii')
      cmd_tokens = string.split(',')
      print(string)
      if cmd_tokens[0] == 'SCHD002':
          print('Received 5 sec scheduler message')
      elif cmd_tokens[0] == 'TELM002':
          print('Received Telemetry Message 002: Sensor telemetry')
          cmd_count = int(cmd_tokens[1])
          err_count = int(cmd_tokens[2])
          temperature = float(cmd_tokens[3])
          pressure = float(cmd_tokens[4])
          altitude = float(cmd_tokens[5]) 
          print temperature, pressure, altitude
          tlm_packet = struct.pack('hhhhfff',0x1002,cmd_count,err_count,0,temperature,pressure,altitude)
          tlm_sock.sendto(tlm_packet, (pictl.UDP_TLM_IP, pictl.UDP_TLM_PORT))
      elif cmd_tokens[0] == 'TELM001':
          print('Received Telemetry Message 001: Executive telemetry')
          cmd_count = int(cmd_tokens[1])
          err_count = int(cmd_tokens[2])
          cfs_running = int(cmd_tokens[3])
          cpu_util = float(cmd_tokens[4])
          tlm_packet = struct.pack('hhhhf',0x1001,cmd_count,err_count,cfs_running,cpu_util)
          tlm_sock.sendto(tlm_packet, (pictl.UDP_TLM_IP, pictl.UDP_TLM_PORT))
           
   except KeyboardInterrupt:
      sys.exit() 


