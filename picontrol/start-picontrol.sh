#!/bin/sh -e
#

#
# PiControl
# Can comment out/clone picontrol-sensor and picontrol-executive if needed
# 
python picontrol-scheduler.py &
python picontrol-command.py &
python picontrol-executive.py &
python picontrol-telemetry.py &

#
# Start one of the sensor support modules
# 
# python /home/pi/PiControl/picontrol/picontrol-adafruit-sensors.py &
python picontrol-enviro-phat.py &

exit 0
