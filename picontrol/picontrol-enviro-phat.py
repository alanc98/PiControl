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
import struct 

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

# Global - LED status
sensor_led_on = 0

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
# pictl.SubscribeToFilter('SCHD001',sub_socket)
pictl.SubscribeToFilter('SENS001',sub_socket)

#
# For Enviro-phat, gather all data and send in TLM packets
# Accept commands to turn LEDs on and off
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
          tlm_packet = struct.pack('8shhhh','TELM001,',0x1004, sensor_cmd_counter, sensor_err_counter , sensor_led_on)
          pub_socket.send(tlm_packet)
          
          #
          # Collect and send telemetry for Temp, Pressure , altitude
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=BMP,CMD=READ,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()
          sensor_tokens = sensor_message.split(',')
          # print sensor_tokens

          temp_string = sensor_tokens[3]
          temp_tokens = temp_string.split('=')
          # print('Temperature = ',temp_tokens[1])
          temperature = float(temp_tokens[1])

          press_string = sensor_tokens[4]
          press_tokens = press_string.split('=')
          # print('Pressure = ', press_tokens[1])
          pressure = float(press_tokens[1])
 
          alt_string = sensor_tokens[5]
          alt_tokens = alt_string.split('=')
          # print('Altitude = ',alt_tokens[1])
          altitude = float(alt_tokens[1])
          tlm_packet = struct.pack('8shhfff','TELM001,',0x1005,0,temperature,pressure,altitude)
             
          pub_socket.send(tlm_packet)

          #
          # end Send tlm for one sensor
          #

          #
          # Collect and send telemetry for light sensor
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=LUX,CMD=READ,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()
          sensor_tokens = sensor_message.split(',')
          print sensor_tokens

          red_string = sensor_tokens[3]
          red_tokens = red_string.split('=')
          # print('RED = ',red_tokens[1])
          red_val = float(red_tokens[1])

          green_string = sensor_tokens[4]
          green_tokens = green_string.split('=')
          # print('green = ', green_tokens[1])
          green_val = float(green_tokens[1])
 
          blue_string = sensor_tokens[5]
          blue_tokens = blue_string.split('=')
          # print('blue = ',blue_tokens[1])
          blue_val = float(blue_tokens[1])
          
          lux_string = sensor_tokens[6]
          lux_tokens = lux_string.split('=')
          # print('lux = ',lux_tokens[1])
          lux_val = float(lux_tokens[1])

          tlm_packet = struct.pack('8shhffff', 'TELM001,',0x1006, 0, red_val, green_val, blue_val, lux_val)
          pub_socket.send(tlm_packet)

          #
          # end Send tlm for one sensor
          #
          
          #
          # Collect and send telemetry for accel sensor
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=ACCEL,CMD=READ,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()
          sensor_tokens = sensor_message.split(',')
          print sensor_tokens

          x_string = sensor_tokens[3]
          x_tokens = x_string.split('=')
          # print('X = ',x_tokens[1])
          x_val = float(x_tokens[1])

          y_string = sensor_tokens[4]
          y_tokens = y_string.split('=')
          # print('Y = ', y_tokens[1])
          y_val = float(y_tokens[1])
 
          z_string = sensor_tokens[5]
          z_tokens = z_string.split('=')
          # print('Z = ',z_tokens[1])
          z_val = float(z_tokens[1])

          tlm_packet = struct.pack('8shhfff','TELM001,',0x1007, 0, x_val, y_val, z_val)
          pub_socket.send(tlm_packet)

          #
          # end Send tlm for one sensor
          #

          #
          # Collect and send telemetry for a sensor
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=HEADING,CMD=READ,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()
          sensor_tokens = sensor_message.split(',')
          print sensor_tokens

          heading_string = sensor_tokens[3]
          heading_tokens = heading_string.split('=')
          # print('Heading = ',heading_tokens[1])
          heading_val = float(heading_tokens[1])

          tlm_packet = struct.pack('8shhf', 'TELM001,', 0x1008, 0, heading_val)
          pub_socket.send(tlm_packet)
          #
          # end Send tlm for one sensor
          #

          #
          # Collect and send telemetry for a sensor
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=MAG,CMD=READ,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()
          sensor_tokens = sensor_message.split(',')
          print sensor_tokens

          x_string = sensor_tokens[3]
          x_tokens = x_string.split('=')
          # print('X = ',x_tokens[1])
          x_val = float(x_tokens[1])

          y_string = sensor_tokens[4]
          y_tokens = y_string.split('=')
          # print('Y = ', y_tokens[1])
          y_val = float(y_tokens[1])
 
          z_string = sensor_tokens[5]
          z_tokens = z_string.split('=')
          # print('Z = ',z_tokens[1])
          z_val = float(z_tokens[1])

          tlm_packet = struct.pack('8shhfff', 'TELM001,', 0x1009, 0, x_val, y_val, z_val)
          pub_socket.send(tlm_packet)
          #
          # end Send tlm for one sensor
          #

      # elif cmd_tokens[0] == 'SCHD001':
      #     print('Received 1hz scheduler message')
      elif cmd_tokens[0] == 'SENS001':

          if cmd_tokens[1] == 'LEDS_ON':
              print('Received SENSOR command - LEDS ON')
              sensor_cmd_counter += 1
              sensor_led_on = 1
              #
              # Send the LED ON command
              #
              sens_srv_socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=LED,CMD=LED_ON,SENSOR_REQ_END")
              sensor_message = sens_srv_socket.recv()

          elif cmd_tokens[1] == 'LEDS_OFF':
             print('Received SENSOR command - LEDS OFF')
             sensor_cmd_counter += 1
             sensor_led_on = 0
             #
             # Send the LED OFF command
             #
             sens_srv_socket.send("SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=LED,CMD=LED_OFF,SENSOR_REQ_END")
             sensor_message = sens_srv_socket.recv()

   except KeyboardInterrupt:
      sys.exit() 
