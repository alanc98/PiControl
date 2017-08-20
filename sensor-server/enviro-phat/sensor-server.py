#
# ZMQ REP Server for the Pimoroni Enviro PHAT for the Raspberry Pi
# Binds REP socket to tcp://*:5555
#
import time
import zmq

# Pimoroni enviro pHat support
import enviro_phat_server

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()

    # Depending on the ID, pass it to the needed sensor function
    message_list = message.split(',')   

    # This is where the right server function is called 
    if message_list[1] == 'DEV=EPH_BMP':
       message = enviro_phat_server.process_bmp_req(message)
    elif message_list[1] == 'DEV=EPH_LIGHT':
       message = enviro_phat_server.process_light_req(message)
    elif message_list[1] == 'DEV=EPH_ACCEL':
       message = enviro_phat_server.process_accel_req(message)
    elif message_list[1] == 'DEV=EPH_HEADING':
       message = enviro_phat_server.process_heading_req(message)
    elif message_list[1] == 'DEV=EPH_MAG':
       message = enviro_phat_server.process_mag_req(message)
    elif message_list[1] == 'DEV=EPH_ANALOG':
       message = enviro_phat_server.process_analog_req(message)
    elif message_list[1] == 'DEV=EPH_LED':
       message = enviro_phat_server.process_led_req(message)
    else:
       # unknown message
       message = "SENSOR_REP," + message_list[1] + ",ERROR=UNKNOWN_ID,SENSOR_REP_END"

    #  Send reply back to client
    socket.send(message)

