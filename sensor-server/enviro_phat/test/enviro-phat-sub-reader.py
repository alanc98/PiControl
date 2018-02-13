from __future__ import print_function
import zmq
import time
import sys

#
# Helper Function to setup a ZMQ subscription
#
def SubscribeToFilter(FilterText, SubSocket):
   if isinstance(FilterText, bytes):
      FilterText = FilterText.decode('ascii')
   SubSocket.setsockopt_string(zmq.SUBSCRIBE, FilterText)

sys.stdout.flush()
context = zmq.Context()
#  Socket to talk to server

# SUB socket to get BMP data
sub_socket = context.socket(zmq.SUB)
sub_socket.connect('tcp://localhost:5559') 
SubscribeToFilter('SENSOR_PUB',sub_socket)

print("Connected")

while True:
  message = sub_socket.recv()
  print("Received PUB message:",message) 

