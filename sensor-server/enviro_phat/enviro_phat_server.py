#
# ZMQ REP Server for the Pimoroni Enviro PHAT for the Raspberry Pi
# Binds REP socket to tcp://*:5555
#
# Todo: Refactor using classes and actual object oriented code.
#
import sys
import time
import zmq
from envirophat import light, weather, motion, analog, leds

global bmp_sub
global bmp_sub_rate
global bmp_sub_ticks
global lux_sub 
global lux_sub_rate 
global lux_sub_ticks 
 
def init_module():
   global bmp_sub 
   global bmp_sub_rate 
   global bmp_sub_ticks 
   global lux_sub 
   global lux_sub_rate 
   global lux_sub_ticks 

   bmp_sub = False   
   bmp_sub_rate = 0
   bmp_sub_ticks = 0
   lux_sub = False   
   lux_sub_rate = 0
   lux_sub_ticks = 0

#
# BMP request function 
#
def process_bmp_req(message):
   global bmp_sub 
   global bmp_sub_rate 
   global bmp_sub_ticks 

   if message_list[3] == 'CMD=READ':
      #
      # Get the values 
      #
      temp = round(weather.temperature(),2)
      pressure = round(weather.pressure(),2)
      altitude = round(weather.altitude(),2)

      #
      # format the message
      #
      message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=BMP,TEMP=%.2f,PRES=%.2f,ALT=%.2f,SENSOR_REP_END" % (temp,pressure,altitude)

   elif message_list[3] == 'CMD=SUB_START':
      rate_message_list = message_list[4].split('=')
      if rate_message_list[0] == 'RATE':
         rate = int(rate_message_list[1])
         if rate < 250:
            bmp_sub_rate = 250 
         else:
            bmp_sub_rate = rate
      bmp_sub_ticks = 0
      bmp_sub = True

      # SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=BMP,CMD=SUB_START,RATE=1000,SENSOR_REQ_END
      # SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=BMP,STATUS=OK|BUSY,SENSOR_REP_END
      message =  "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=BMP,STATUS=OK,SENSOR_REP_END"

   elif message_list[3] == 'CMD=SUB_STOP':
 
      bmp_sub = False
      bmp_sub_rate = 0
      bmp_sub_ticks = 0

      # SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=BMP,CMD=SUB_STOP,SENSOR_REQ_END
      # SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=BMP,STATUS=OK,SENSOR_REP_END
      message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=BMP,STATUS=OK,SENSOR_REP_END"

   else:
      # unknown Command
      message = "SENSOR_REP," + message_list[1] + ",SUB_DEV=BMP,ERROR=UNKNOWN_CMD,SENSOR_REP_END"

   #
   #  Send reply back to client
   #
   return message

#
# Light request function 
#
def process_light_req(message):
   global lux_sub 
   global lux_sub_rate 
   global lux_sub_ticks 

   if message_list[3] == 'CMD=READ':
      # Get the values 
      s_red, s_green, s_blue = light.rgb()
      s_lux = light.light()
 
      # format the message
      message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=LUX,RED=%.2f,GREEN=%.2f,BLUE=%.2f,LUX=%.2f,SENSOR_REP_END" % (s_red,s_green,s_blue, s_lux)

   elif message_list[3] == 'CMD=SUB_START':
      rate_message_list = message_list[4].split('=')
      if rate_message_list[0] == 'RATE':
         rate = int(rate_message_list[1])
         if rate < 250:
            lux_sub_rate = 250 
         else:
            lux_sub_rate = rate
      lux_sub_ticks = 0
      lux_sub = True

      # SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=LUX,CMD=SUB_START,RATE=1000,SENSOR_REQ_END
      # SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=LUX,STATUS=OK|BUSY,SENSOR_REP_END
      message =  "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=LUX,STATUS=OK,SENSOR_REP_END"

   elif message_list[3] == 'CMD=SUB_STOP':
 
      lux_sub = False
      lux_sub_rate = 0
      lux_sub_ticks = 0

      # SENSOR_REQ,DEV=ENVIRO_PHAT,SUB_DEV=LUX,CMD=SUB_STOP,SENSOR_REQ_END
      # SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=LUX,STATUS=OK,SENSOR_REP_END
      message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=LUX,STATUS=OK,SENSOR_REP_END"

   else:
      # unknown Command
      message = "SENSOR_REP," + message_list[1] + ",SUB_DEV=LUX,ERROR=UNKNOWN_CMD,SENSOR_REP_END"
   #  Send reply back to client
   return message

#
# Accel request function 
#
def process_accel_req(message):

   # Get the values 
   s_x, s_y, s_z = motion.accelerometer()
 
   # format the message
   message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=ACCEL,X=%.2f,Y=%.2f,Z=%.2f,SENSOR_REP_END" % (s_x,s_y,s_z)

   #  Send reply back to client
   return message


#
# Heading request function 
#
def process_heading_req(message):

   # Get the values 
   s_heading = motion.heading()
 
   # format the message
   message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=HEADING,HEADING=%.2f,SENSOR_REP_END" % (s_heading)

   #  Send reply back to client
   return message


#
# Mag values request function 
#
def process_mag_req(message):

   # Get the values 
   s_x, s_y, s_z = motion.magnetometer()
 
   # format the message
   message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=MAG,X=%.2f,Y=%.2f,Z=%.2f,SENSOR_REP_END" % (s_x,s_y,s_z)

   #  Send reply back to client
   return message


#
# Analog input request function 
#
def process_analog_req(message):

   # Get the values 
   s_a1, s_a2, s_a3, s_a4 = analog.read_all()
 
   # format the message
   message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=ANALOG,A1=%.2f,A2=%.2f,A3=%.2f,A4=%.2f,SENSOR_REP_END" % (s_a1,s_a2,s_a3,s_a4)

   #  Send reply back to client
   return message


#
# LED request function 
#
def process_led_req(message):

   led_message_list = message.split(',')
   if led_message_list[3] == 'CMD=LED_ON':
      leds.on()
      message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=LED,LED=ON,SENSOR_REP_END"
   else:
      leds.off()
      message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=LED,LED=OFF,SENSOR_REP_END"

   #  Send reply back to client
   return message

#
# High level sensor subscription processing function
# 
def process_sensor_subs(tick):
   global bmp_sub 
   global bmp_sub_rate 
   global bmp_sub_ticks 
   global lux_sub 
   global lux_sub_rate 
   global lux_sub_ticks 

   if bmp_sub == True:
      bmp_sub_ticks += 250
      if bmp_sub_ticks >= bmp_sub_rate:
         #
         # Get the values 
         #
         temp = round(weather.temperature(),2)
         pressure = round(weather.pressure(),2)
         altitude = round(weather.altitude(),2)

         time_string = time.time()
         #
         # format the message
         #
         message = "SENSOR_PUB,DEV=ENVIRO_PHAT,SUB_DEV=BMP,TIME=%s,TEMP=%.2f,PRES=%.2f,ALT=%.2f,SENSOR_PUB_END" % (time_string,temp,pressure,altitude)
         pub_socket.send_string(message)
         bmp_sub_ticks = 0
   if lux_sub == True:
      lux_sub_ticks += 250
      if lux_sub_ticks >= lux_sub_rate:
         #
         # Get the values 
         #
         s_red, s_green, s_blue = light.rgb()
         s_lux = light.light()
         time_string = time.time()
 
         # format the message
         message = "SENSOR_PUB,DEV=ENVIRO_PHAT,SUB_DEV=LUX,TIME=%s,RED=%.2f,GREEN=%.2f,BLUE=%.2f,LUX=%.2f,SENSOR_PUB_END" % (time_string,s_red,s_green,s_blue, s_lux)
         pub_socket.send_string(message)
         lux_sub_ticks = 0

#
# High level sensor request function
#
def process_sensor_req(message):
   # Depending on the ID, pass it to the needed sensor function
   message_list = message.split(',')   

   # This is where the right server function is called 
   if message_list[2] == 'SUB_DEV=BMP':
      message = process_bmp_req(message)
   elif message_list[2] == 'SUB_DEV=LUX':
      message = process_light_req(message)
   elif message_list[2] == 'SUB_DEV=ACCEL':
      message = process_accel_req(message)
   elif message_list[2] == 'SUB_DEV=HEADING':
      message = process_heading_req(message)
   elif message_list[2] == 'SUB_DEV=MAG':
       message = process_mag_req(message)
   elif message_list[2] == 'SUB_DEV=ANALOG':
      message = process_analog_req(message)
   elif message_list[2] == 'SUB_DEV=LED':
      message = process_led_req(message)
   else:
      # unknown message
      message = "SENSOR_REP," + message_list[1] + ",ERROR=UNKNOWN_ID,SENSOR_REP_END"

   return message

#
# Init globals
# 
init_module()

#
# Setup ZMQ sockets
#
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

#
# Socket for PUB status messages
#
pub_socket = context.socket(zmq.PUB)
pub_socket.bind('tcp://*:5559')

tick = 0

while True:
   try:
      # Poll the socket for a message with a timeout
      status = socket.poll(timeout=250)

      if status == 0:
         tick += 1
         if tick == 5:
            tick = 0
         process_sensor_subs(tick) 
            
      else:
         #  Wait for next request from client
         message = socket.recv()

         # Depending on the ID, pass it to the needed sensor function
         message_list = message.split(',')   

         # This is where the right server function is called 
         if message_list[1] == 'DEV=ENVIRO_PHAT':
            message = process_sensor_req(message)
         else:
            # unknown message
            message = "SENSOR_REP," + message_list[1] + ",ERROR=UNKNOWN_ID,SENSOR_REP_END"

         #  Send reply back to client
         socket.send(message)

   except KeyboardInterrupt:    
      sys.exit()

