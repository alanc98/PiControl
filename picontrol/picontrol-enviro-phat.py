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
pictl.SubscribeToFilter('SENS002',sub_socket)

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
          telemetry_string = 'TELM004,' + str(sensor_cmd_counter) + ',' \
                             + str(sensor_err_counter) + \
                             ',' + str(sensor_led_on) 
          print telemetry_string
          pub_socket.send_string(telemetry_string)
          
          #
          # Collect and send telemetry for Temp, Pressure , altitude
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=EPH_BMP,CMD=READ,SENSOR_REQ_END")
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
          
          telemetry_string = 'TELM005,' + temp_tokens[1] + ',' \
                             + press_tokens[1] + ',' + alt_tokens[1] 
          print telemetry_string
          pub_socket.send_string(telemetry_string)
          #
          # end Send tlm for one sensor
          #

          #
          # Collect and send telemetry for light sensor
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=EPH_LIGHT,CMD=READ,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()
          sensor_tokens = sensor_message.split(',')
          print sensor_tokens

          red_string = sensor_tokens[2]
          red_tokens = red_string.split('=')
          # print('RED = ',red_tokens[1])

          green_string = sensor_tokens[3]
          green_tokens = green_string.split('=')
          # print('green = ', green_tokens[1])
 
          blue_string = sensor_tokens[4]
          blue_tokens = blue_string.split('=')
          # print('blue = ',blue_tokens[1])
          
          lux_string = sensor_tokens[5]
          lux_tokens = lux_string.split('=')
          # print('lux = ',lux_tokens[1])

          telemetry_string = 'TELM006,' + red_tokens[1] + ',' + green_tokens[1] + \
                             ',' + blue_tokens[1] + ',' + lux_tokens[1]
          print telemetry_string
          pub_socket.send_string(telemetry_string)
          #
          # end Send tlm for one sensor
          #
          
          #
          # Collect and send telemetry for accel sensor
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=EPH_ACCEL,CMD=READ,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()
          sensor_tokens = sensor_message.split(',')
          print sensor_tokens

          x_string = sensor_tokens[2]
          x_tokens = x_string.split('=')
          # print('X = ',x_tokens[1])

          y_string = sensor_tokens[3]
          y_tokens = y_string.split('=')
          # print('Y = ', y_tokens[1])
 
          z_string = sensor_tokens[4]
          z_tokens = z_string.split('=')
          # print('Z = ',z_tokens[1])

          telemetry_string = 'TELM007,' + x_tokens[1] + ',' + y_tokens[1] + ',' + z_tokens[1]   
          print telemetry_string
          pub_socket.send_string(telemetry_string)

          #
          # end Send tlm for one sensor
          #

          #
          # Collect and send telemetry for a sensor
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=EPH_HEADING,CMD=READ,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()
          sensor_tokens = sensor_message.split(',')
          print sensor_tokens

          heading_string = sensor_tokens[2]
          heading_tokens = heading_string.split('=')
          # print('Heading = ',heading_tokens[1])

          telemetry_string = 'TELM008,' + heading_tokens[1]  
          print telemetry_string
          pub_socket.send_string(telemetry_string)
          #
          #
          # end Send tlm for one sensor
          #

          #
          # Collect and send telemetry for a sensor
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=EPH_MAG,CMD=READ,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()
          sensor_tokens = sensor_message.split(',')
          print sensor_tokens

          x_string = sensor_tokens[2]
          x_tokens = x_string.split('=')
          # print('X = ',x_tokens[1])

          y_string = sensor_tokens[3]
          y_tokens = y_string.split('=')
          # print('Y = ', y_tokens[1])
 
          z_string = sensor_tokens[4]
          z_tokens = z_string.split('=')
          # print('Z = ',z_tokens[1])

          telemetry_string = 'TELM009,' + x_tokens[1] + ',' + y_tokens[1] + ',' + z_tokens[1]   
          print telemetry_string
          pub_socket.send_string(telemetry_string)
          #
          # end Send tlm for one sensor
          #

      # elif cmd_tokens[0] == 'SCHD001':
      #     print('Received 1hz scheduler message')
      elif cmd_tokens[0] == 'SENS001':
          print('Received SENSOR command 001 - LEDS ON')
          sensor_cmd_counter += 1
          sensor_led_on = 1
          #
          # Send the LED ON command
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=EPH_LED,CMD=LED_ON,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()

      elif cmd_tokens[0] == 'SENS002':
          print('Received SENSOR command 002 - LEDS OFF')
          sensor_cmd_counter += 1
          sensor_led_on = 0
          #
          # Send the LED OFF command
          #
          sens_srv_socket.send("SENSOR_REQ,DEV=EPH_LED,CMD=LED_OFF,SENSOR_REQ_END")
          sensor_message = sens_srv_socket.recv()

   except KeyboardInterrupt:
      sys.exit() 
