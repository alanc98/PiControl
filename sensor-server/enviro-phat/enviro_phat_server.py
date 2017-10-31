
import sys
import time
from envirophat import light, weather, motion, analog, leds

#
# BMP request function 
#
def process_bmp_req(message):

   # Get the values 
   temp = round(weather.temperature(),2)
   pressure = round(weather.pressure(),2)
   altitude = round(weather.altitude(),2)
 
   # format the message
   message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=BMP,TEMP=%.2f,PRES=%.2f,ALT=%.2f,SENSOR_REP_END" % (temp,pressure,altitude)

   #  Send reply back to client
   return message

#
# Light request function 
#
def process_light_req(message):

   # Get the values 
   s_red, s_green, s_blue = light.rgb()
   s_lux = light.light()
 
   # format the message
   message = "SENSOR_REP,DEV=ENVIRO_PHAT,SUB_DEV=LUX,RED=%.2f,GREEN=%.2f,BLUE=%.2f,LUX=%.2f,SENSOR_REP_END" % (s_red,s_green,s_blue, s_lux)

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

