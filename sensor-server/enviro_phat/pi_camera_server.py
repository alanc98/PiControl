
import sys
import time
import threading
from   picamera import PiCamera

#
# Capture a picture ( worker thread )
#
def capture_still(image_size, vflip, hflip, file):
   camera = PiCamera()
   
   if image_size == 1:
      camera.resolution = (1024,768)
   elif image_size == 2:
      camera.resolution = (1920,1080)
   else:
      camera.resolution = (2592,1944)

   if vflip == True:
      camera.vflip = True

   if hflip == True:
      camera.hflip = True

   camera.capture(file)
  
   camera.close()
 
   return 
   
#
# STILL request function 
#
# SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=STILL,CMD=CAPTURE,SIZE=1,VFLIP=TRUE,FILE=test1.jpg,SENSOR_REQ_END
#
#
def process_still_req(message):

   cam_message_list = message.split(',')
   print(cam_message_list)

   size_list = cam_message_list[4].split('=')
   print(size_list)

   vflip_list = cam_message_list[5].split('=')
   print(vflip_list)

   file_list = cam_message_list[6].split('=')
   print(file_list)

   # Gather and convert parameters
   if size_list[1] == '1':
      ImageSize = 1
   elif size_list[1] == '2':
      ImageSize = 2
   else:
      ImageSize = 3

   if vflip_list[1] == 'TRUE':
      Vflip = True
   else:
      Vflip = False

   # call thread  
   capture_still(ImageSize, Vflip, True, file_list[1])
 
   message = "SENSOR_REP,DEV=PI_CAMERA,SUB_DEV=STILL,STATUS=OK,SENSOR_REP_END"

   return message

#
# Capture a Video ( worker thread )
#
def capture_video(image_size, vflip, hflip, file, duration):
   camera = PiCamera()

   print('capture_video -- file is', file)
   
   if image_size == 1:
      camera.resolution = (640,480)
   elif image_size == 2:
      camera.resolution = (1280,720)
   else:
      camera.resolution = (1920,1080)

   if vflip == True:
      camera.vflip = True

   if hflip == True:
      camera.hflip = True

   camera.start_recording(file)
   camera.wait_recording(duration)
   camera.stop_recording()
   camera.close()
   return 

#
# VID request function 
#
# SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=VIDEO,CMD=CAPTURE,SIZE=1,VFLIP=TRUE,FILE=test1.h264,DURATION=10,SENSOR_REQ_END
#
def process_video_req(message):
   cam_message_list = message.split(',')
   print(cam_message_list)

   size_list = cam_message_list[4].split('=')
   print(size_list)

   vflip_list = cam_message_list[5].split('=')
   print(vflip_list)

   duration_list = cam_message_list[6].split('=')
   print(duration_list)

   file_list = cam_message_list[7].split('=')
   print(file_list)

   # Gather and convert parameters
   if size_list[1] == '1':
      ImageSize = 1
   elif size_list[1] == '2':
      ImageSize = 2
   else:
      ImageSize = 3

   if vflip_list[1] == 'TRUE':
      Vflip = True
   else:
      Vflip = False

   print (duration_list[1])
   Duration = int(duration_list[1]) 

   # call thread  
   capture_video(ImageSize, Vflip, True, file_list[1], Duration)

   message = "SENSOR_REP,DEV=PI_CAMERA,SUB_DEV=VIDEO,STATUS=OK,SENSOR_REP_END"

   return message

#
# TIMELAPSE request function 
#
# SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=TIMELAPSE,CMD=CAPTURE,SIZE=1,VFLIP=TRUE,DELAY=10,FRAMES=10,SENSOR_REQ_END
#
def process_timelapse_req(message):
   cam_message_list = message.split(',')
   print(cam_message_list)
   message = "SENSOR_REP,DEV=PI_CAMERA,SUB_DEV=TIMELAPSE,STATUS=OK,SENSOR_REP_END"

   return message

#
# High level sensor request function
#
def process_sensor_req(message):
   # Depending on the ID, pass it to the needed sensor function
   message_list = message.split(',')   

   # This is where the right server function is called 
   if message_list[2] == 'SUB_DEV=STILL':
      message = process_still_req(message) 
   elif message_list[2] == 'SUB_DEV=VIDEO':
      message = process_video_req(message) 
   elif message_list[2] == 'SUB_DEV=TIMELAPSE':
      message = process_timelapse_req(message)
   else:
      # unknown message
      message = "SENSOR_REP," + message_list[2] + ",ERROR=UNKNOWN_SUB_ID,SENSOR_REP_END"

   return message

