#!/bin/sh -e
#

#
# PiControl
# Can comment out/clone picontrol-sensor and picontrol-executive if needed
# 
python picontrol_scheduler.py &
python picontrol_command.py &
python picontrol_executive.py &
python picontrol_telemetry.py &

#
# Start one or more of the sensor support modules
# 
# python /home/pi/PiControl/picontrol/picontrol_adafruit_sensors.py &
python picontrol_enviro_phat.py &
python picontrol_pi_camera.py &

exit 0
