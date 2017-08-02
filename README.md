# PiControl
Framework for remote control / data collection of embedded raspberry pi apps

This is a simple Command and Telemetry framework written in Python, and using the ZeroMQ message library. It includes a COSMOS ground system target with a few simple commands and telemetry packets. 

The primary use is to control the cFS ( see cfs.gsfc.nasa.gov ) running on a Raspberry Pi or Pi-Sat. 

If you want to have it control other programs on the Pi, see the file picontrol-executive.py, and also the constants file pictl.py. 

NOTE: The Pi is commanded through this framework via unencrypted UDP packet. It is not secure for apps on the internet!!!

It is intended for projects that are on a local/private network!


