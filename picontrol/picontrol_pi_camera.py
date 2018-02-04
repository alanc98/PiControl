#
#   PiControl Pi Camera Process   
#   This Process sends commands to the sensor server to control the Raspberry Pi Camera 
# 
#   Subscribes to:
#     Commands: localhost  ZMQ_COMMAND_PORT 
#     Scheduler: localhost ZMQ_SCHEDULER_PORT 
# 
#   Publishes: 
#     Telemetry: localhost ZMQ_CAMERA_PORT  
# 
#   Uses REQ/REP Socket: ZMQ_PI_CAMERA_SENSOR_PORT
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
camera_cmd_counter = 0

# Global - Command error counter
camera_err_counter = 0

# Global - camera status
camera_status = 0

# Global - seconds count
camera_video_seconds = 0

# Global - timelapse frame count
camera_timelapse_frames = 0

# Global ZeroMQ context
context = zmq.Context()

# Command Socket 
sub_socket = context.socket(zmq.SUB)
sub_socket.connect('tcp://localhost:' + pictl.ZMQ_SCHEDULER_PORT)
sub_socket.connect('tcp://localhost:' + pictl.ZMQ_COMMAND_PORT)
sub_socket.connect('tcp://localhost:' + pictl.ZMQ_PI_CAMERA_STATUS_PUB_PORT)

# Telemety Socket  
pub_socket = context.socket(zmq.PUB)
pub_socket.bind('tcp://*:' + pictl.ZMQ_CAMERA_PORT)

# Sensor server Socket
sens_srv_socket = context.socket(zmq.REQ)
sens_srv_socket.connect('tcp://localhost:' + pictl.ZMQ_PI_CAMERA_SENSOR_PORT)

#
# Setup subscription filters
#
pictl.SubscribeToFilter('SCHD002',sub_socket)
pictl.SubscribeToFilter('PCAM001',sub_socket)
pictl.SubscribeToFilter('SENSOR_PUB',sub_socket)

#
# Accept commands to capture pictures, videos, or timelapse sequences
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
          tlm_packet = struct.pack('8shhhhhh','TELM001,',0x100A, camera_cmd_counter, camera_err_counter , camera_status, camera_video_seconds,camera_timelapse_frames)
          pub_socket.send(tlm_packet)
          
      elif cmd_tokens[0] == 'SENSOR_PUB':
          print('Video Status:' + string)
          if cmd_tokens[1] == 'DEV=PI_CAMERA':
             video_status_tokens = cmd_tokens[2].split('=')
             if video_status_tokens[0] == 'VIDEO_SECOND':
                camera_video_seconds = int(video_status_tokens[1]) 
             elif video_status_tokens[0] == 'VIDEO_DONE':
                camera_status = 0 
                camera_video_seconds = 0
             elif video_status_tokens[0] == 'TIMELAPSE_FRAME':
                camera_timelapse_frames = int(video_status_tokens[1]) 
             elif video_status_tokens[0] == 'TIMELAPSE_DONE':
                camera_status = 0 
                camera_timelapse_frames = 0

             tlm_packet = struct.pack('8shhhhhh','TELM001,',0x100A, camera_cmd_counter, camera_err_counter , camera_status, camera_video_seconds,camera_timelapse_frames)
             pub_socket.send(tlm_packet)
          
      # elif cmd_tokens[0] == 'SCHD001':
      #     print('1hz scheduler message')
      elif cmd_tokens[0] == 'PCAM001':

          if cmd_tokens[1] == 'NOOP':
              print('Received PiCam command - NOOP')
              camera_cmd_counter += 1
          #
          # What params does the capture image command need?
          #    Size, Vflip, file
          # PCAM001,CAPTURE_IMAGE,SIZE_1,VFLIP_ON,40 string
          if cmd_tokens[1] == 'CAPTURE_IMAGE':
              cmd_error = False
              print('Received PICAM command - CAPTURE_IMAGE')
              if cmd_tokens[2] == 'SIZE_1':
                 size_var = 'SIZE=1'
              elif cmd_tokens[2] == 'SIZE_2':
                 size_var = 'SIZE=2'
              elif cmd_tokens[2] == 'SIZE_3':
                 size_var = 'SIZE=3'
              else:
                 camera_err_counter += 1
                 print('Invalid SIZE specified in CAPTURE_IMAGE command')
                 continue
                 
              if cmd_tokens[3] == 'VFLIP_ON':
                 flip_var = 'VFLIP=TRUE'
              elif cmd_tokens[3] == 'VFLIP_OF':
                 flip_var = 'VFLIP=FALSE'
              else:
                 camera_err_counter += 1
                 print('Invalid VFLIP specified in CAPTURE_IMAGE command')
                 continue
  
              file_name = cmd_tokens[4]
              camera_cmd_counter += 1
              #
              # Send the CAPTURE_IMAGE command
              #
              sensor_cmd = 'SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=STILL,CMD=CAPTURE,' + size_var + ',' \
                           + flip_var + ',FILE=' + file_name + ',SENSOR_REQ_END'
              print ('sending: ' , sensor_cmd )
              sens_srv_socket.send_string(sensor_cmd)
              sensor_message = sens_srv_socket.recv()

          # --------------------------------------------------------------------------------------
          elif cmd_tokens[1] == 'CAPTURE_VIDEO':
              if camera_status == 1:
                 camera_err_counter += 1
                 print('Camera is busy!')
                 continue

              cmd_error = False
              print('Received PICAM command - CAPTURE_VIDEO')
              if cmd_tokens[2] == 'SIZE_1':
                 size_var = 'SIZE=1'
              elif cmd_tokens[2] == 'SIZE_2':
                 size_var = 'SIZE=2'
              elif cmd_tokens[2] == 'SIZE_3':
                 size_var = 'SIZE=3'
              else:
                 camera_err_counter += 1
                 print('Invalid SIZE specified in CAPTURE_VIDEO command')
                 continue
                 
              if cmd_tokens[3] == 'VFLIP_ON':
                 flip_var = 'VFLIP=TRUE'
              elif cmd_tokens[3] == 'VFLIP_OF':
                 flip_var = 'VFLIP=FALSE'
              else:
                 camera_err_counter += 1
                 print('Invalid VFLIP specified in CAPTURE_VIDEO command')
                 continue
       
              # Duration of video capture
              duration = cmd_tokens[4].lstrip('0')
              duration = cmd_tokens[4].lstrip(' ')

              # video filename
              file_name = cmd_tokens[5]

              #
              # Send the CAPTURE_VIDEO command
              #
              sensor_cmd = 'SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=VIDEO,CMD=CAPTURE,' + size_var + ',' \
                           + flip_var + ',DURATION=' + duration + ',FILE=' + file_name + ',SENSOR_REQ_END'
              print ('sending: ' , sensor_cmd )
              sens_srv_socket.send_string(sensor_cmd)
              sensor_message = sens_srv_socket.recv()
              sensor_msg_tokens = sensor_message.split(',')
              if sensor_msg_tokens[3] == 'STATUS=OK':
                 camera_cmd_counter += 1
                 camera_status = 1
              else:
                 camera_err_counter += 1
          # --------------------------------------------------------------------------------------
          # Timelapse:
          #   Parameters are:
          #      SIZE_1 | SIZE_2 | SIZE_3 
          #      VFLIP_ON | VFLIP_OF
          #      integer delay in seconds between frames
          #      integer number of frames to capture
          #      filename prefix 
          #
          elif cmd_tokens[1] == 'CAPTURE_TIMELAPSE':
              if camera_status == 1:
                 camera_err_counter += 1
                 print('Camera is busy!')
                 continue

              cmd_error = False
              print('Received PICAM command - CAPTURE_TIMELAPSE')
              if cmd_tokens[2] == 'SIZE_1':
                 size_var = 'SIZE=1'
              elif cmd_tokens[2] == 'SIZE_2':
                 size_var = 'SIZE=2'
              elif cmd_tokens[2] == 'SIZE_3':
                 size_var = 'SIZE=3'
              else:
                 camera_err_counter += 1
                 print('Invalid SIZE specified in CAPTURE_TIMELAPSE command')
                 continue
                 
              if cmd_tokens[3] == 'VFLIP_ON':
                 flip_var = 'VFLIP=TRUE'
              elif cmd_tokens[3] == 'VFLIP_OF':
                 flip_var = 'VFLIP=FALSE'
              else:
                 camera_err_counter += 1
                 print('Invalid VFLIP specified in CAPTURE_TIMELAPSE command')
                 continue
       
              # Delay 
              delay_val = cmd_tokens[4].lstrip('0')
              delay_val = cmd_tokens[4].lstrip(' ')

              # Frames
              num_frames = cmd_tokens[5].lstrip('0')
              num_frames = cmd_tokens[5].lstrip(' ')

              # timelaspse filename prefix
              file_prefix = cmd_tokens[6]

              #
              # Send the CAPTURE_TIMELAPSE command
              #
              #   Parameters are:
              #      SIZE ( 1, 2, or 3 ) 
              #      VFLIP ( TRUE or FALSE )
              #      FILE_PRE = ( filename prefix string )
              #      DELAY = ( integer delay in seconds between frames )
              #      FRAMES = ( integer number of frames to capture )
              #
              # SENSOR_REQ,
              #             DEV=PI_CAMERA,SUB_DEV=TIMELAPSE,CMD=CAPTURE,SIZE=1,VFLIP=TRUE,FILE_PRE=timelapse-,
              #             DELAY=10,FRAMES=10,
              # SENSOR_REQ_END
              #
              sensor_cmd = 'SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=TIMELAPSE,CMD=CAPTURE,' + size_var + ',' \
                           + flip_var + ',FILE_PRE=' + file_prefix + ',DELAY=' + delay_val + ',FRAMES=' + num_frames + ',SENSOR_REQ_END'
              print ('sending: ' , sensor_cmd )
              sens_srv_socket.send_string(sensor_cmd)
              sensor_message = sens_srv_socket.recv()
              sensor_msg_tokens = sensor_message.split(',')
              if sensor_msg_tokens[3] == 'STATUS=OK':
                 camera_cmd_counter += 1
                 camera_status = 1
              else:
                 camera_err_counter += 1
          # --------------------------------------------------------------------------------------
              

   except KeyboardInterrupt:
      sys.exit() 
