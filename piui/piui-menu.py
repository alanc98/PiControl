# 
# PiUi menu system for Adafruit SSD1306 display
#
#  For the Raspberry Pi computer. 
#  Menus are controlled by switch buttons connected to GPIO pins
#  Currently setup for 3 buttons:
#  Up = GPIO 20
#  Down = GPIO 21
#  Select = GPIO 26
#
#  (c) 2017 Alan Cudmore
# 
# Uses original SSD1306 code: 
#   Copyright (c) 2014 Adafruit Industries
#   by: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#

import time
import os
import sys
import subprocess
import psutil
import socket
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#
# Image file for logo
# 
LOGO_IMAGE = '/home/pi/PiControl/piui/pisat_logo_64.png'

#
# Button - sleep delay
#
SLEEP_DELAY = 0.04

#
# Constants for PiControl commands ( Start and Stop cFS )
#
PICONTROL_UDP_IP    = "127.0.0.1"
PICONTROL_UDP_PORT  = 8080 
PICONTROL_CFS_START = "EXEC001,START_CFS"
PICONTROL_CFS_STOP  = "EXEC002,STOP_CFS"

# 
# Raspberry Pi SPI pin configuration:
#
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 
# Initialize the 128x64 display with hardware SPI
#
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

#
# Globals
#
menu_item_selected = 1
cfs_is_running = 0

#
# Draw the Main Menu Screen
#
def DrawMainMenuScreen(menu_item,cfs_running):
   disp.clear()
   disp.display()

   # Create blank image for drawing.
   # Make sure to create image with mode '1' for 1-bit color.
   width = disp.width
   height = disp.height
   image = Image.new('1', (width, height))

   # Get drawing object to draw on image.
   draw = ImageDraw.Draw(image)

   # Draw some shapes.
   # First define some constants to allow easy resizing of shapes.
   padding = 2
   top = padding
   bottom = height-padding
   # Move left to right keeping track of the current x position for drawing shapes.
   x = padding

   # Load default font.
   font = ImageFont.load_default()

   # Shell scripts for system monitoring from here: 
   #  https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
   cmd = "hostname -I | cut -d\' \' -f1"
   IP = subprocess.check_output(cmd, shell = True )
   CPU = psutil.cpu_percent(interval=None)
   # Write two lines of text.
   draw.text((x, top), 'IP: ' + str(IP),  font=font, fill=255)
   top += 8
   draw.text((x, top),  'CPU: ' + str(CPU) + '%', font=font, fill=255)
   top += 8
   if cfs_running == 0:
      draw.text((x, top), 'CFE: *Not Running* ', font=font, fill=255)
   else:
      draw.text((x, top), 'CFE: *Running*', font=font, fill=255)
   top += 8
   if menu_item == 1:
      if cfs_running == 0:
         draw.text((x, top), '[*] Start cFE', font=font, fill=255)
      else:
         draw.text((x, top), '[*] Stop cFE', font=font, fill=255)
   else:
      if cfs_running == 0:
         draw.text((x, top), '[ ] Start cFE', font=font, fill=255)
      else:
         draw.text((x, top), '[ ] Stop cFE', font=font, fill=255)
   top += 8
   if menu_item == 2:
      draw.text((x, top), '[*] Reboot Pi-Sat' , font=font, fill=255)
   else:
      draw.text((x, top), '[ ] Reboot Pi-Sat' , font=font, fill=255)
   top += 8
   if menu_item == 3:
      draw.text((x, top), '[*] Halt Pi-Sat' , font=font, fill=255)
   else:
      draw.text((x, top), '[ ] Halt Pi-Sat' , font=font, fill=255)
   top += 8
   if menu_item == 4:
      draw.text((x, top), '[*] Exit Menu' , font=font, fill=255)
   else:
      draw.text((x, top), '[ ] Exit Menu' , font=font, fill=255)

   # Display image.
   disp.image(image)
   disp.display()

#
# Draw the "Are you Sure?" screen 
#
def DrawAreYouSureScreen(text_prompt,menu_item):
   disp.clear()
   disp.display()

   # Create blank image for drawing.
   # Make sure to create image with mode '1' for 1-bit color.
   width = disp.width
   height = disp.height
   image = Image.new('1', (width, height))

   # Get drawing object to draw on image.
   draw = ImageDraw.Draw(image)

   # Draw some shapes.
   # First define some constants to allow easy resizing of shapes.
   padding = 2
   top = padding
   bottom = height-padding
   # Move left to right keeping track of the current x position for drawing shapes.
   x = padding

   # Load default font.
   font = ImageFont.load_default()

   # Write two lines of text.
   draw.text((x, top), text_prompt,  font=font, fill=255)
   top += 8
   draw.text((x, top),  'Are you sure?', font=font, fill=255)
   top += 8
   if menu_item == 1:
      draw.text((x, top), '[*] No, Cancel' , font=font, fill=255)
   else:
      draw.text((x, top), '[ ] No, Cancel' , font=font, fill=255)
   top += 8
   if menu_item == 2:
      draw.text((x, top), '[*] Yes!' , font=font, fill=255)
   else:
      draw.text((x, top), '[ ] Yes!' , font=font, fill=255)

   # Display image.
   disp.image(image)
   disp.display()

#
# Draw the "Wait for Reboot" screen 
#
def DrawWaitForRebootScreen():
   disp.clear()
   disp.display()

   # Create blank image for drawing.
   # Make sure to create image with mode '1' for 1-bit color.
   width = disp.width
   height = disp.height
   image = Image.new('1', (width, height))

   # Get drawing object to draw on image.
   draw = ImageDraw.Draw(image)

   # Draw some shapes.
   # First define some constants to allow easy resizing of shapes.
   padding = 2
   top = padding
   bottom = height-padding
   # Move left to right keeping track of the current x position for drawing shapes.
   x = padding

   # Load default font.
   font = ImageFont.load_default()

   # Write two lines of text.
   top += 8
   draw.text((x, top), '***** REBOOTING *****',  font=font, fill=255)
   top += 16 
   draw.text((x, top), ' Please wait 30 secs', font=font, fill=255)
   top += 8
   draw.text((x, top), ' Until Logo is back' , font=font, fill=255)
   top += 16 
   draw.text((x, top), '* DO NOT POWER OFF! *' , font=font, fill=255)

   # Display image.
   disp.image(image)
   disp.display()

#
# Draw the "Wait for Shutdown" screen 
#
def DrawWaitForShutdownScreen():
   disp.clear()
   disp.display()

   # Create blank image for drawing.
   # Make sure to create image with mode '1' for 1-bit color.
   width = disp.width
   height = disp.height
   image = Image.new('1', (width, height))

   # Get drawing object to draw on image.
   draw = ImageDraw.Draw(image)

   # Draw some shapes.
   # First define some constants to allow easy resizing of shapes.
   padding = 2
   top = padding
   bottom = height-padding
   # Move left to right keeping track of the current x position for drawing shapes.
   x = padding

   # Load default font.
   font = ImageFont.load_default()

   # Write two lines of text.
   draw.text((x, top), '*** SHUTTING DOWN ***' ,  font=font, fill=255)
   top += 16 
   draw.text((x, top), ' Please wait 30 secs'  , font=font, fill=255)
   top += 8
   draw.text((x, top), '  Until shutdown is    ' , font=font, fill=255)
   top += 8 
   draw.text((x, top), '      Complete   '     , font=font, fill=255)
   top += 16 
   draw.text((x, top), 'Then switch off power' , font=font, fill=255)

   # Display image.
   disp.image(image)
   disp.display()
#
# Initialize Display library.
# 
disp.begin()

#
# Setup GPIO buttons
#
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#
# Create UDP socket to send commands to PiControl
#
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

#
# Start of main loop 
#
while 1:

   #
   # Display Bootup Logo
   #
   disp.clear()
   disp.display()
   image = Image.open(LOGO_IMAGE).convert('1')
   disp.image(image)
   disp.display()

   #
   # Wait until the user presses a button before displaying menu
   #
   exit_logo = False
   while exit_logo == False:
      if (GPIO.input(20) == False):
         exit_logo = True
      elif (GPIO.input(21) == False):
         exit_logo = True
      elif (GPIO.input(26)== False):
         exit_logo = True
      time.sleep(SLEEP_DELAY);

   #
   # Now display the menu and poll for input from user
   #
   DrawMainMenuScreen(menu_item_selected,cfs_is_running)

   exit_menu = False  
   while exit_menu == False:
      if (GPIO.input(20) == False):
         if menu_item_selected == 1:
            menu_item_selected = 4
         else:
           menu_item_selected -= 1
         DrawMainMenuScreen(menu_item_selected,cfs_is_running)
      elif (GPIO.input(21) == False):
         if menu_item_selected == 4:
            menu_item_selected = 1
         else:
            menu_item_selected += 1
         DrawMainMenuScreen(menu_item_selected,cfs_is_running)
      elif (GPIO.input(26)== False):
         if menu_item_selected == 1:
            if cfs_is_running == 0:
               sock.sendto(PICONTROL_CFS_START, (PICONTROL_UDP_IP, PICONTROL_UDP_PORT))
               cfs_is_running = 1
            else:
               sock.sendto(PICONTROL_CFS_STOP, (PICONTROL_UDP_IP, PICONTROL_UDP_PORT))
               cfs_is_running = 0
            DrawMainMenuScreen(menu_item_selected,cfs_is_running)
         elif menu_item_selected == 2:
            #
            # User selected the second menu item ( reboot ) 
            # Display submenu
            #
            reboot_menu_item = 1 
            DrawAreYouSureScreen('Reboot Pi',reboot_menu_item)
            exit_sure_menu = False  
            while exit_sure_menu == False:
               time.sleep(SLEEP_DELAY);
               if (GPIO.input(20) == False):
                  if reboot_menu_item == 1:
                     reboot_menu_item = 2 
                  else:
                     reboot_menu_item = 1
                  DrawAreYouSureScreen('Reboot Pi',reboot_menu_item)
               elif (GPIO.input(21) == False):
                  if reboot_menu_item == 1:
                     reboot_menu_item = 2 
                  else:
                     reboot_menu_item = 1
                  DrawAreYouSureScreen('Reboot Pi',reboot_menu_item)
               elif (GPIO.input(26)== False):
                  if reboot_menu_item == 2:
                     #
                     # Display Wait for reboot Screen
                     #
                     DrawWaitForRebootScreen()
                     print 'Rebooting Pi!!!!'
                     reboot_output = subprocess.check_output('reboot', shell = True )
                     exit_sure_menu = True
                  else:
                     exit_sure_menu = True
            DrawMainMenuScreen(menu_item_selected,cfs_is_running)
            # end of processing menu item 2
         elif menu_item_selected == 3:
            #
            # User selected the Third menu item ( Shutdown ) 
            # Display submenu
            #
            shutdown_menu_item = 1 
            DrawAreYouSureScreen('Shutdown Pi',shutdown_menu_item)
            exit_sure_menu = False  
            while exit_sure_menu == False:
               time.sleep(SLEEP_DELAY);
               if (GPIO.input(20) == False):
                  if shutdown_menu_item == 1:
                     shutdown_menu_item = 2 
                  else:
                     shutdown_menu_item = 1
                  DrawAreYouSureScreen('Shutdown Pi',shutdown_menu_item)
               elif (GPIO.input(21) == False):
                  if shutdown_menu_item == 1:
                     shutdown_menu_item = 2 
                  else:
                     shutdown_menu_item = 1
                  DrawAreYouSureScreen('Shutdown Pi',shutdown_menu_item)
               elif (GPIO.input(26)== False):
                  if shutdown_menu_item == 2:
                     #
                     # Display Wait for shutdown screen
                     #
                     DrawWaitForShutdownScreen()
                     print 'Shutting Down Pi!!!!'
                     shutdown_output = subprocess.check_output('halt', shell = True )
                     exit_sure_menu = True
                  else:
                     exit_sure_menu = True
            DrawMainMenuScreen(menu_item_selected,cfs_is_running)
            # end of processing menu item 2
            print 'Shut Down Pi-Sat!'
         elif menu_item_selected == 4:
            # Exit back to logo 
            exit_menu = True 
        
      time.sleep(SLEEP_DELAY);
    
