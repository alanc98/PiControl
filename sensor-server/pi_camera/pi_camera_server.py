import sys
import time
import zmq
import threading
from   picamera import PiCamera

global camera_busy 
global camera_abort 

def init_module():
   global camera_busy 
   global camera_abort
   camera_busy = False
   camera_abort = False

#
# Capture a picture 
#
def capture_still(image_size, vflip, file):
   camera = PiCamera()
   
   if image_size == 1:
      camera.resolution = (1024,768)
   elif image_size == 2:
      camera.resolution = (1920,1080)
   else:
      camera.resolution = (2592,1944)

   if vflip == True:
      camera.vflip = True
      camera.hflip = True

   try:
      camera.capture(file)
      camera.close()
      return True 
   except: 
      camera.close()
      return False 
   
#
# STILL request function 
#
# SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=STILL,CMD=CAPTURE,SIZE=1,VFLIP=TRUE,FILE=test1.jpg,SENSOR_REQ_END
#
#
def process_still_req(message):
   global camera_busy 

   if camera_busy == True:
      message = "SENSOR_REP,DEV=PI_CAMERA,SUB_DEV=STILL,STATUS=ERROR_BUSY,SENSOR_REP_END"
      return message
   else:
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

      # call Helper thread  
      cam_result = capture_still(ImageSize, Vflip, file_list[1])

      if cam_result == True: 
         message = "SENSOR_REP,DEV=PI_CAMERA,SUB_DEV=STILL,STATUS=OK,SENSOR_REP_END"
      else:
         message = "SENSOR_REP,DEV=PI_CAMERA,SUB_DEV=STILL,STATUS=ERROR,SENSOR_REP_END"

      return message

#
# Capture a Video ( worker thread )
#   Idea is to spawn a thread to perform this function
#   The thread could publish status update messages 
#   If a new thread is spawned for the video it will have to keep a new request 
#   from being processed, since the camera is busy 
#
def capture_video(image_size, vflip, file, duration):
   global camera_busy 
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
      camera.hflip = True

   camera.start_recording(file)
   for i in range (duration):
      video_status_string = 'SENSOR_PUB,DEV=PI_CAMERA,SUB_DEV=VIDEO,VIDEO_SECOND=' + str(i) + ',SENSOR_PUB_END'
      pub_socket.send_string(video_status_string)
      camera.wait_recording(1)
   video_status_string = 'SENSOR_PUB,DEV=PI_CAMERA,SUB_DEV=VIDEO,VIDEO_SECOND=DONE,SENSOR_PUB_END'
   pub_socket.send_string(video_status_string)

   camera.stop_recording()
   camera.close()
   camera_busy = False 
   return 

#
# VIDEO request function 
#
# SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=VIDEO,CMD=CAPTURE,SIZE=1,VFLIP=TRUE,FILE=test1.h264,DURATION=10,SENSOR_REQ_END
#
def process_video_req(message):
   global camera_busy 

   if camera_busy == True:
      message = "SENSOR_REP,DEV=PI_CAMERA,SUB_DEV=VIDEO,STATUS=ERROR_BUSY,SENSOR_REP_END"
      return message
   else:
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

      # Create thread to capture the video
      video_thread = threading.Thread(target=capture_video, args=(ImageSize, Vflip, file_list[1], Duration))
      video_thread.start()
      camera_busy = True 

      message = "SENSOR_REP,DEV=PI_CAMERA,SUB_DEV=VIDEO,STATUS=OK,SENSOR_REP_END"
      return message

#
# Capture a Timelapse ( worker thread )
#   Idea is to spawn a thread to perform this function
#   The thread could publish status update messages 
#   If a new thread is spawned for the timelapse it will have to keep a new request 
#   from being processed, since the camera is busy 
#
def capture_timelapse(image_size, vflip, file_prefix, delay, frames):
   global camera_busy 
   camera = PiCamera()

   print('capture_timelapse -- file prefix is', file_prefix)
   
   if image_size == 1:
      camera.resolution = (1024,768)
   elif image_size == 2:
      camera.resolution = (1920,1080)
   else:
      camera.resolution = (2592,1944)

   if vflip == True:
      camera.vflip = True
      camera.hflip = True

   for i in range(frames):
      filename = file_prefix + '%04d.jpg' % i
      print('Capturing file %s' % filename)
      camera.capture(filename)
      timelapse_status_string = 'SENSOR_PUB,DEV=PI_CAMERA,SUB_DEV=TIMELAPSE,TIMELAPSE_FRAME=' + str(i) + ',SENSOR_PUB_END'
      pub_socket.send_string(timelapse_status_string)
      time.sleep(delay)
 
   timelapse_status_string = 'SENSOR_PUB,DEV=PI_CAMERA,SUB_DEV=TIMELAPSE,TIMELAPSE_FRAME=DONE,SENSOR_PUB_END'
   pub_socket.send_string(timelapse_status_string)

   camera.close()
   camera_busy = False 
   return 

#
# TIMELAPSE request function 
#
# SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=TIMELAPSE,CMD=CAPTURE,SIZE=1,VFLIP=TRUE,FILE_PRE=timelapse-,DELAY=10,FRAMES=10,SENSOR_REQ_END
#
# Timelapse parameters include:
#   Size
#   Vflip
#   File Prefix
#   Delay between frames
#   Number of Frames to capture
#
def process_timelapse_req(message):
   global camera_busy 
   if camera_busy == True:
      message = "SENSOR_REP,DEV=PI_CAMERA,SUB_DEV=TIMELAPSE,STATUS=ERROR_BUSY,SENSOR_REP_END"
      return message
   else:
      cam_message_list = message.split(',')
      print(cam_message_list)

      size_list = cam_message_list[4].split('=')
      print(size_list)

      vflip_list = cam_message_list[5].split('=')
      print(vflip_list)

      file_prefix_list = cam_message_list[6].split('=')
      print(file_prefix_list)

      delay_list = cam_message_list[7].split('=')
      print(delay_list)

      frames_list = cam_message_list[8].split('=')
      print(frames_list)

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

      print (delay_list[1])
      Delay = int(delay_list[1]) 

      print (frames_list[1])
      Frames = int(frames_list[1])

      # Create thread to capture the video
      video_thread = threading.Thread(target=capture_timelapse, args=(ImageSize, Vflip, file_prefix_list[1], Delay, Frames))
      video_thread.start()
      camera_busy = True 

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

#
# ZMQ REP Server for the Raspberry Pi Camera
# Binds REP socket to tcp://*:5557
#

context = zmq.Context()

#
# Socket for REQ/REP messages
#
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5557")

#
# Socket for PUB status messages
# 
pub_socket = context.socket(zmq.PUB)
pub_socket.bind('tcp://*:5558')


# Need to initalize the global variables first
init_module()

while True:
   try:
      #  Wait for next request from client
      message = socket.recv()

      # Depending on the ID, pass it to the needed sensor function
      message_list = message.split(',')   

      if message_list[1] == 'DEV=PI_CAMERA':
         message = process_sensor_req(message)

      else:
         # unknown message
         message = "SENSOR_REP," + message_list[1] + ",ERROR=UNKNOWN_ID,SENSOR_REP_END"

      #  Send reply back to client
      socket.send(message)
   except KeyboardInterrupt:    
      sys.exit()
