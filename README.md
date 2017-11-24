![Pi Control Logo by Michael Cudmore](/images/PiControl_Logo_v1.jpg)

# PiControl

A Framework for remote control and data collection from Raspberry Pi Sensors and Apps. 

This is a simple Command and Telemetry framework written in Python using the ZeroMQ message library. It includes a COSMOS ground system target (see cosmosrb.com ) with simple commands and telemetry packets. 

The primary use is to start and stop the cFS ( see https://cfs.gsfc.nasa.gov ) running on a Raspberry Pi or Pi-Sat. It has been expanded to provide telemetry for the Pimoroni Enviro Phat and other HATs can be added.   

If you want to have it control other programs on the Pi, see the file picontrol-executive.py, and also the constants file pictl.py. 

The picontrol framework gets data from the sensors by using ZeroMQ request/reply messages to a sensor-server. The sensor-server takes avantage of example python code to read data from the sensors. This python code must be installed for the sensors that are being read ( Pimoroni Enviro Phat for example ). The sensor-server can also be used by other programs such as the cFS to read sensor data.          

The piui program is a somewhat related program to control a user interface via Adafruit SPI SSD1306 OLED screen ( 128x64 pixels ). The menus are controlled by buttons connected to GPIO inputs on the Pi. The only real connection is that it can be used to send commands to the picontrol framework. 

NOTE: The Pi is commanded through this framework via unencrypted UDP packet. It is not secure for apps on the internet!!!

It is intended for projects that are on a local/private network! Don't put this on a network where security is a concern ( or use it for command and control of devices that are important )

I'm still learning how I can efficiently fit this all together (Python and ZeroMQ), so I may be shuffling things around. 

