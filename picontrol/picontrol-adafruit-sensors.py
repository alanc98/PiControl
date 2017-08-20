#
#   PiControl Sensor Process   
#   This Process Collects data from a sensor server and sends the values in telemetry 
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

import pictl

#
# Globals for telemetry
#

# process number
global proc

# Global - Command counter
sensor_cmd_counter = 0

# Global - Command error counter
sensor_err_counter = 0

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
pictl.SubscribeToFilter('SENS001',sub_socket)
# pictl.SubscribeToFilter('SCHD001',sub_socket)


while True:
   try:
      string = sub_socket.recv_string()
      string = string.decode('ascii')
      cmd_tokens = string.split(',')
      print(string)
      if cmd_tokens[0] == 'SCHD002':
          sens_srv_socket.send("SENSOR_REQ,BMP180,CMD=READ,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()
          sensor_tokens = sensor_message.split(',')
          # print sensor_tokens

          temp_string = sensor_tokens[2]
          temp_tokens = temp_string.split('=')
          # print('Temperature = ',temp_tokens[1])

          press_string = sensor_tokens[3]
          press_tokens = press_string.split('=')
          # print('Pressure = ', press_tokens[1])
 
          alt_string = sensor_tokens[4]
          alt_tokens = alt_string.split('=')
          # print('Altitude = ',alt_tokens[1])
          
          telemetry_string = 'TELM002,' + str(sensor_cmd_counter) + ',' + str(sensor_err_counter) + ',' + temp_tokens[1] + ',' + press_tokens[1] + ',' + alt_tokens[1] 
          print telemetry_string
          pub_socket.send_string(telemetry_string)
      # elif cmd_tokens[0] == 'SCHD001':
      #     print('Received 1hz scheduler message')
      elif cmd_tokens[0] == 'SENS001':
          print('Received SENSOR command 001')
          sensor_cmd_counter += 1
   except KeyboardInterrupt:
      sys.exit() 
