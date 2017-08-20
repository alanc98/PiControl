#
#   PiControl command input process
#
#   Reads from UDP port from an external command source 
#   Binds PUB socket to ZMQ_COMMAND_PORT 
#
#   Subscribes to:
#     Currently nothing - may want to subscribe to housekeeping requests
#
import sys
import zmq
import time
import socket

import pictl

UDP_IP = "0.0.0.0"

#
# Bind to the UDP socket
#
udp_socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
udp_socket.bind((UDP_IP, pictl.UDP_COMMAND_PORT))

#
# Bind to the ZeroMQ socket to publish commands
#
context = zmq.Context()
zmq_socket = context.socket(zmq.PUB)
zmq_socket.bind('tcp://*:' + pictl.ZMQ_COMMAND_PORT)

while True:
   try: 
      data, addr = udp_socket.recvfrom(1024) # buffer size is 1024 bytes
      # print "received message:", data
      zmq_socket.send_string(data)
      # print "sent message on zmq socket"
   except KeyboardInterrupt:
      sys.exit()
