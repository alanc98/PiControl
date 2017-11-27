#
#   PiControl Constants and functions
#    This should become a class 
# 

import zmq

#
# ZeroMQ message ports for REQ/REP
# 
ZMQ_ENIVRO_PHAT_PORT = '5555'
ZMQ_ADAFRUIT_PORT    = '5556'
ZMQ_PI_CAMERA_PORT   = '5557'

#
# ZeroMQ message ports ( for PUB )
#
ZMQ_SCHEDULER_PORT = '5560'
ZMQ_COMMAND_PORT   = '5561'
ZMQ_EXECUTIVE_PORT = '5562'
ZMQ_SENSOR_PORT    = '5563'
ZMQ_CAMERA_PORT    = '5564'

#
# UDP port for external commands
# 
UDP_COMMAND_PORT = 8080

#
# This is the IP address where the picontrol telemetry process
# will send it's telemetry packets
# This will change depending on your ground system host
#
# UDP_TLM_IP = '192.168.1.2'
UDP_TLM_IP = '127.0.0.1'

# 
# This is the port for the picontrol telemetry process
# 
UDP_TLM_PORT = 8081

#
# Executive ( cFS manager ) 
# Change the path depending on where the cFS is located on your Pi 
# 
CFS_PATH = '/home/pi/pisat/cfs/build/exe/cpu1'
CFS_BINARY = './core-cpu1'

#
# Helper Function to setup a ZMQ subscription
#
def SubscribeToFilter(FilterText, SubSocket):
   if isinstance(FilterText, bytes):
      FilterText = FilterText.decode('ascii')
   SubSocket.setsockopt_string(zmq.SUBSCRIBE, FilterText)

