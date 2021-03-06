#
#   PiControl Executive Process   
#   This Process executes commands sent from the ground system or UI
#   It also reports simple telemetry values
#   It currently executes commands to start the cFS software, stop the cFS, 
#   reboot the Pi, and Shutdown the Pi
# 
#   Subscribes to:
#     Commands: localhost  ZMQ_COMMAND_PORT 
#     Scheduler: localhost ZMQ_SCHEDULER_PORT 
# 
#   Publishes: 
#     Telemetry: localhost ZMQ_EXECUTIVE_PORT  
#
# Todo: Break apart into main and helper functions
#       Preferably break this apart into a class with global variables in the class
#  
import sys
import zmq
import subprocess
import time
import psutil
import struct

import pictl

#
# Globals for telemetry
#

# process number
global proc

# Global - is the cFS running?
exec_cfs_started = 0 

# Global - Command counter
exec_cmd_counter = 0

# Global - Command error counter
exec_err_counter = 0

# Global - CPU Utilization
exec_cpu_utilization = 0.0

# Global ZeroMQ context
context = zmq.Context()

# Command Socket 
sub_socket = context.socket(zmq.SUB)
sub_socket.connect('tcp://localhost:' + pictl.ZMQ_SCHEDULER_PORT)
sub_socket.connect('tcp://localhost:' + pictl.ZMQ_COMMAND_PORT)

# Telemety Socket  
pub_socket = context.socket(zmq.PUB)
pub_socket.bind('tcp://*:' + pictl.ZMQ_EXECUTIVE_PORT)

#
# Setup subscription filters
#
pictl.SubscribeToFilter('SCHD002',sub_socket)
# pictl.SubscribeToFilter('SCHD001',sub_socket)
pictl.SubscribeToFilter('EXEC001',sub_socket)

while True:
   try:
      string = sub_socket.recv_string()
      string = string.decode('ascii')
      cmd_tokens = string.split(',')
      print(string)
      if cmd_tokens[0] == 'SCHD002':
         exec_cpu_utilization = psutil.cpu_percent()
         telemetry_packet = struct.pack('8shhhhf','TELM001,',0x1001,exec_cmd_counter,exec_err_counter,exec_cfs_started,exec_cpu_utilization)
         pub_socket.send(telemetry_packet)

      elif cmd_tokens[0] == 'EXEC001':
         if cmd_tokens[1] == 'START_CFS':
            print('Received EXEC command START_CFS')
            if exec_cfs_started == 1:
               exec_err_counter += 1
               print('ERROR: cFS is already running')   
            else:
               try:
                  proc = subprocess.Popen([pictl.CFS_BINARY], cwd=pictl.CFS_PATH, shell=False)
                  print('  Process started:',proc.pid)
                  exec_cmd_counter += 1
                  exec_cfs_started = 1 
               except:
                  exec_err_counter += 1
                  exec_cfs_started = 1
         elif cmd_tokens[1] == 'NOOP':
            print('Received EXEC command - NOOP')
            exec_cmd_counter += 1
         elif cmd_tokens[1] == 'REBOOT':
            print('Received EXEC command - Reboot')
            proc = subprocess.Popen('reboot', shell=False)
            exec_cmd_counter += 1
         elif cmd_tokens[1] == 'SHUTDOWN':
            print('Received EXEC Halt command')
            proc = subprocess.Popen('halt', shell=False)
            exec_cmd_counter += 1
         elif cmd_tokens[1] == 'STOP_CFS':
            print('Received EXEC command 004')
            if exec_cfs_started == 1:
               print('Kill the cFS process')
               subprocess.call(["kill", "-9", "%d" % proc.pid])
               proc.wait()
               exec_cfs_started = 0 
               exec_cmd_counter += 1
            else:
               print('Error: cFS is not running, nothing to kill')
               exec_cfs_started = 0 
               exec_err_counter += 1
   except KeyboardInterrupt:
      if exec_cfs_started == True:
         print('Intercepted Control-C, exiting')
         subprocess.call(["kill", "-9", "%d" % proc.pid])
         proc.wait()
         exec_cfs_started = False
      sys.exit() 
