import sys
import time
from envirophat import light, weather, motion, analog, leds

def process_bmp_req(message):

   # Get the values 
   temp = round(weather.temperature(),2)
   pressure = round(weather.pressure(),2)
   altitude = round(weather.altitude(),2)
 
   # format the message
   message = "SENSOR_REP,DEV=EPH_BMP,TEMP=%.2f,PRES=%.2f,ALT=%.2f,SENSOR_REP_END" % (temp,pressure,altitude)

   #  Send reply back to client
   return message


def process_light_req(message):

   # Get the values 
   s_red, s_green, s_blue = light.rgb()
   s_lux = light.light()
 
   # format the message
   message = "SENSOR_REP,DEV=EPH_LIGHT,RED=%.2f,GREEN=%.2f,BLUE=%.2f,LUX=%.2f,SENSOR_REP_END" % (s_red,s_green,s_blue, s_lux)

   #  Send reply back to client
   return message

def process_accel_req(message):

   # Get the values 
   s_x, s_y, s_z = motion.accelerometer()
 
   # format the message
   message = "SENSOR_REP,DEV=EPH_ACCEL,X=%.2f,Y=%.2f,Z=%.2f,SENSOR_REP_END" % (s_x,s_y,s_z)

   #  Send reply back to client
   return message

def process_heading_req(message):

   # Get the values 
   s_heading = motion.heading()
 
   # format the message
   message = "SENSOR_REP,DEV=EPH_HEADING,HEADING=%.2f,SENSOR_REP_END" % (s_heading)

   #  Send reply back to client
   return message

def process_mag_req(message):

   # Get the values 
   s_x, s_y, s_z = motion.magnetometer()
 
   # format the message
   message = "SENSOR_REP,DEV=EPH_MAG,X=%.2f,Y=%.2f,Z=%.2f,SENSOR_REP_END" % (s_x,s_y,s_z)

   #  Send reply back to client
   return message

def process_analog_req(message):

   # Get the values 
   s_a1, s_a2, s_a3, s_a4 = analog.read_all()
 
   # format the message
   message = "SENSOR_REP,DEV=EPH_ANALOG,A1=%.2f,A2=%.2f,A3=%.2f,A4=%.2f,SENSOR_REP_END" % (s_a1,s_a2,s_a3,s_a4)

   #  Send reply back to client
   return message


def process_led_req(message):

   led_message_list = message.split(',')
   if led_message_list[2] == 'CMD=LED_ON':
      leds.on()
      message = "SENSOR_REP,DEV=EPH_LED,LED=ON,SENSOR_REP_END"
   else:
      leds.off()
      message = "SENSOR_REP,DEV=EPH_LED,LED=OFF,SENSOR_REP_END"

   #  Send reply back to client
   return message
