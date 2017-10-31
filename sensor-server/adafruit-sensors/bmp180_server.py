import Adafruit_BMP.BMP085 as BMP085

def process_req(message):

   sensor = BMP085.BMP085(busnum=1)

   # Get the values 
   temp              = sensor.read_temperature()
   pressure          = sensor.read_pressure()
   altitude          = sensor.read_altitude()
   sealevel_pressure = sensor.read_sealevel_pressure()
 
   # format the message
   message = "SENSOR_REP,DEV=ADA_BMP180,SUB_DEV=BMP,TEMP=%.2f,PRES=%.2f,ALT=%.2f,SL_PRES=%.2f,SENSOR_REP_END" % (temp,pressure,altitude,sealevel_pressure)

   #  Send reply back to client
   return message

