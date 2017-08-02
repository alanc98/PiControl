#
#   PiControl scheduler process
#    Sends out periodic packets to schedule PiControl apps 
#
#   Binds PUB socket to tcp://*:ZMQ_SCHEDULER_PORT
#
import zmq
import sys
import time

import pictl

context = zmq.Context()

socket = context.socket(zmq.PUB)
socket.bind('tcp://*:' + pictl.ZMQ_SCHEDULER_PORT)

wakeup_counter = 0

while True:
   try:
      time.sleep(1)
      wakeup_counter += 1
      socket.send_string('SCHD001,CMD=WAKE_1_SEC')
      # print('sent 1_SEC scheduler packet')

      if wakeup_counter == 5:
          socket.send_string('SCHD002,CMD=WAKE_5_SEC')
          wakeup_counter = 0
          # print('sent 5_SEC scheduler packet')
   except KeyboardInterrupt:
      sys.exit()
