# 
# tsl_lux_server
#
import time
import zmq
from   tsl2561 import TSL2561

def process_req(message):
    tsl=TSL2561(busnum=1)

    # Get the values 
    lux_value = tsl.lux() 
 
    # format the message
    message = "SENSOR_REP,DEV=ADA_TSL2561,SUB_DEV=LUX,LUX=%d,SENSOR_REP_STOP" % (lux_value)

    # Return the message
    return message
