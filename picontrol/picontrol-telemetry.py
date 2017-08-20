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


#
# Setup subscription filters
#
pictl.SubscribeToFilter('SCHD002',socket)
pictl.SubscribeToFilter('TELM001',socket)
pictl.SubscribeToFilter('TELM002',socket)
pictl.SubscribeToFilter('TELM003',socket)
pictl.SubscribeToFilter('TELM004',socket)
pictl.SubscribeToFilter('TELM005',socket)
pictl.SubscribeToFilter('TELM006',socket)

while True:
   try:
      string = socket.recv_string()
      string = string.decode('ascii')
      cmd_tokens = string.split(',')
      print(string)
      if cmd_tokens[0] == 'SCHD002':
          print('Received 5 sec scheduler message')
      elif cmd_tokens[0] == 'TELM001':
          print('Received Telemetry Message 001: Executive telemetry')
          cmd_count = int(cmd_tokens[1])
          err_count = int(cmd_tokens[2])
          cfs_running = int(cmd_tokens[3])
          cpu_util = float(cmd_tokens[4])
          tlm_packet = struct.pack('hhhhf',0x1001,cmd_count,err_count,cfs_running,cpu_util)
          try:
             tlm_sock.sendto(tlm_packet, (pictl.UDP_TLM_IP, pictl.UDP_TLM_PORT))
          except:
             print ('Could not send packet on UDP port')
      elif cmd_tokens[0] == 'TELM002':
          print('Received Telemetry Message 002: Sensor telemetry')
          cmd_count = int(cmd_tokens[1])
          err_count = int(cmd_tokens[2])
          temperature = float(cmd_tokens[3])
          pressure = float(cmd_tokens[4])
          altitude = float(cmd_tokens[5]) 
          print temperature, pressure, altitude
          tlm_packet = struct.pack('hhhhfff',0x1002,cmd_count,err_count,0,temperature,pressure,altitude)
          try:
             tlm_sock.sendto(tlm_packet, (pictl.UDP_TLM_IP, pictl.UDP_TLM_PORT))
          except:
             print ('Could not send packet on UDP port')
      elif cmd_tokens[0] == 'TELM003':
          print('Received Telemetry Message 003: Light Sensor TLM')
          red_val = float(cmd_tokens[1])
          green_val = float(cmd_tokens[2])
          blue_val = float(cmd_tokens[3])
          lux_val = float(cmd_tokens[4])
          tlm_packet = struct.pack('hhffff',0x1003,0,red_val, green_val, blue_val, lux_val)
          try:
             tlm_sock.sendto(tlm_packet, (pictl.UDP_TLM_IP, pictl.UDP_TLM_PORT))
          except:
             print ('Could not send packet on UDP port')
      elif cmd_tokens[0] == 'TELM004':
          print('Received Telemetry Message 004: Accel TLM')
          x_val = float(cmd_tokens[1])
          y_val = float(cmd_tokens[2])
          z_val = float(cmd_tokens[3])
          tlm_packet = struct.pack('hhfff',0x1004,0,x_val, y_val, z_val)
          try:
             tlm_sock.sendto(tlm_packet, (pictl.UDP_TLM_IP, pictl.UDP_TLM_PORT))
          except:
             print ('Could not send packet on UDP port')
      elif cmd_tokens[0] == 'TELM005':
          print('Received Telemetry Message 005: Heading TLM')
          heading_val = float(cmd_tokens[1])
          print ('telemetry sending heading val = ',heading_val)
          tlm_packet = struct.pack('hhf',0x1005,0,heading_val)
          try:
             tlm_sock.sendto(tlm_packet, (pictl.UDP_TLM_IP, pictl.UDP_TLM_PORT))
          except:
             print ('Could not send packet on UDP port')
      elif cmd_tokens[0] == 'TELM006':
          print('Received Telemetry Message 006: Mag TLM')
          x_val = float(cmd_tokens[1])
          y_val = float(cmd_tokens[2])
          z_val = float(cmd_tokens[3])
          tlm_packet = struct.pack('hhfff',0x1006,0,x_val, y_val, z_val)
          try:
             tlm_sock.sendto(tlm_packet, (pictl.UDP_TLM_IP, pictl.UDP_TLM_PORT))
          except:
             print ('Could not send packet on UDP port')
      else:
          print ('unknown telemetry packet')
           
   except KeyboardInterrupt:
      sys.exit() 


