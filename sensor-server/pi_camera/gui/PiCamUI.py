#
# sensor server picam module GUI
#
from   PyQt4 import QtGui
from   PyQt4.QtCore import QThread, SIGNAL
import sys 
import time 
import zmq

import PiCamUIDesign 

#
# Globals for this module
#  The globals are needed between the GUI class and the Thread that receives
#  ZeroMQ sub packets
#  The GUI class connects to the socket because the user can set the IP address
#  The Thread needs access to the socket to receive the sub packets.
# 
#  Maybe a better approach would be to use a signal from the GUI class to the 
#  thread class to set the IP address.
# 
global __sub_socket__
global __sub_socket_connected__

#
# The PiCamUI Thread to receive Zero MQ Sub/Pub packets
#
class PiCamUIThread(QThread):

   def __init__(self):
      QThread.__init__(self)

   def __del__(self):
      print 'UI Thread ending'
      self.wait()

   def run(self):
      global __sub_socket__
      global __sub_socket_connected__

      counter = 1

      while True:
         if __sub_socket_connected__ == True:
            # Read and process the PUB messages
            status_message = __sub_socket__.recv()
            status_message_list = status_message.split(',')
            if status_message_list[2] == 'SUB_DEV=VIDEO':
               if status_message_list[3] == 'VIDEO_SECOND=DONE':
                  self.emit(SIGNAL('update_camera_status(QString)'),'IDLE') 
               else:
                  seconds_list = status_message_list[3].split('=')
                  seconds = seconds_list[1]
                  self.emit(SIGNAL('update_video_counter(QString)'),seconds) 
            elif status_message_list[2] == 'SUB_DEV=TIMELAPSE':
               if status_message_list[3] == 'TIMELAPSE_FRAME=DONE':
                  self.emit(SIGNAL('update_camera_status(QString)'),'IDLE') 
               else:
                  frames_list = status_message_list[3].split('=')
                  frames = frames_list[1]
                  self.emit(SIGNAL('update_timelapse_frames(QString)'),frames) 
         else:
            time.sleep(2)
 
class PiCamUIApp(QtGui.QMainWindow, PiCamUIDesign.Ui_MainWindow):
   def __init__(self):
      global __sub_socket__
      global __sub_socket_connected__

      super(self.__class__, self).__init__()
      self.setupUi(self) 

      # Populate Combo-boxes
      self.imageSizeComboBox.addItem("1024x768")
      self.imageSizeComboBox.addItem("1920x1080")
      self.imageSizeComboBox.addItem("2592x1944")
      self.videoSizeComboBox.addItem("640x480")
      self.videoSizeComboBox.addItem("1280x720")
      self.videoSizeComboBox.addItem("1920x1080")
      self.timelapseSizeComboBox.addItem("1024x768")
      self.timelapseSizeComboBox.addItem("1920x1080")
      self.timelapseSizeComboBox.addItem("2592x1944")

      # Pre-populate the Filename/Path text boxes
      self.imagePathLineEdit.setText("/home/pi/Pictures/picam_image001.jpg")
      self.videoPathLineEdit.setText("/home/pi/Pictures/picam_video001.h264")
      self.timelapsePathLineEdit.setText("/home/pi/Pictures/timelapse-01-")

      # Pre-populate IP address and ports
      self.ipAddressLineEdit.setText("127.0.0.1")
      self.reqPortLineEdit.setText("5557")
      self.subPortLineEdit.setText("5558")

      # Pre-populate Camera Status
      self.cameraStatusLineEdit.setText("IDLE")
      self.videoSecondsLineEdit.setText("0")
      self.timelapseFramesLineEdit.setText("0")

      # Connect buttons
      self.imagePushButton.clicked.connect(self.send_capture_image_message) 
      self.videoPushButton.clicked.connect(self.send_capture_video_message) 
      self.timelapsePushButton.clicked.connect(self.send_capture_timelapse_message) 
      self.ConnectPushButton.clicked.connect(self.connect_to_ports) 
      self.connected = False

      # setup ZMQ context and create sockets
      # Note that the sub_socket is global to the module because
      # the thread needs to receive the SUB/PUB packets
      self.context = zmq.Context()
      self.req_socket = self.context.socket(zmq.REQ)
      self.req_socket_connected = False
      __sub_socket__ = self.context.socket(zmq.SUB)
      __sub_socket_connected__ = False

      self.uiThread = PiCamUIThread()
      self.connect(self.uiThread, SIGNAL("update_video_counter(QString)"),self.update_video_counter)
      self.connect(self.uiThread, SIGNAL("update_camera_status(QString)"),self.update_camera_status)
      self.connect(self.uiThread, SIGNAL("update_timelapse_frames(QString)"),self.update_timelapse_frames)
      self.uiThread.start()

      # Camera Busy indication
      self.camera_is_busy = False

   def SubscribeToFilter(self, FilterText, SubSocket):
      if isinstance(FilterText, bytes):
         FilterText = FilterText.decode('ascii')
      SubSocket.setsockopt_string(zmq.SUBSCRIBE, FilterText)

   def update_video_counter(self,counter_text):
      self.videoSecondsLineEdit.setText(counter_text)

   def update_timelapse_frames(self,frames_text):
      self.timelapseFramesLineEdit.setText(frames_text)

   def update_camera_status(self,status_text):
      self.cameraStatusLineEdit.setText(status_text)

   def send_camera_sensor_req(self, req_message):
      print req_message
      if self.req_socket_connected == True:
         self.req_socket.send(str(req_message))
         reply_message = self.req_socket.recv()
         print 'Received Pi_Camera sensor reply:' , reply_message
      else:
         print 'Socket not connected'

   def connect_to_ports(self):
      global __sub_socket__
      global __sub_socket_connected__

      if self.req_socket_connected == False:
         ip_addr = self.ipAddressLineEdit.text()
         ip_string = 'tcp://' + ip_addr + ':5557'
         self.req_socket.connect(str(ip_string))
         self.req_socket_connected = True
         self.connectedCheckBox.setChecked(True)
      else:
         self.connectedCheckBox.setChecked(True)

      if __sub_socket_connected__ == False:
         ip_addr = self.ipAddressLineEdit.text()
         ip_string = 'tcp://' + ip_addr + ':5558'
         __sub_socket__.connect(str(ip_string))
         self.SubscribeToFilter('SENSOR_PUB',__sub_socket__)
         __sub_socket_connected__ = True

   def send_capture_image_message(self):
      image_size_text = self.imageSizeComboBox.currentText()
      if image_size_text == '1024x768':
          message_size_text = '1'
      elif image_size_text == '1920x1080':
          message_size_text = '2'
      else:
          message_size_text = '3'
      image_file_name = self.imagePathLineEdit.text()
      if self.imageCheckBox.isChecked() == True:
          flip_text = 'TRUE'
      else:
          flip_text = 'FALSE'
      sensor_req_message = 'SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=STILL,CMD=CAPTURE,SIZE=' + message_size_text + ',VFLIP=' + flip_text + ',FILE=' + image_file_name + ',SENSOR_REQ_END'
      self.send_camera_sensor_req(sensor_req_message)

   def send_capture_video_message(self):
      video_size_text = self.videoSizeComboBox.currentText()
      if video_size_text == '640x480':
          size_text = '1'
      elif video_size_text == '1280x720':
          size_text = '2'
      else:
          size_text = '3'
      video_file_name = self.videoPathLineEdit.text()
      if self.videoCheckBox.isChecked() == True:
          flip_text = 'TRUE'
      else:
          flip_text = 'FALSE'
      video_seconds = self.videoLengthSpinBox.value()
      duration_text = str(video_seconds)

      sensor_req_message = 'SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=VIDEO,CMD=CAPTURE,SIZE=' + size_text + ',VFLIP=' + flip_text + ',DURATION=' + duration_text + ',FILE=' + video_file_name + ',SENSOR_REQ_END'
      self.cameraStatusLineEdit.setText("BUSY")
      self.send_camera_sensor_req(sensor_req_message)

 
   def send_capture_timelapse_message(self):
      image_size_text = self.timelapseSizeComboBox.currentText()
      if image_size_text == '1024x768':
          message_size_text = '1'
      elif image_size_text == '1920x1080':
          message_size_text = '2'
      else:
          message_size_text = '3'
      image_file_prefix = self.timelapsePathLineEdit.text()
      if self.timelapseCheckBox.isChecked() == True:
          flip_text = 'TRUE'
      else:
          flip_text = 'FALSE'
      num_frames_text = str(self.timelapseFramesSpinBox.value())
      frame_delay_text = str(self.timelapseDelaySpinBox.value())
      sensor_req_message = 'SENSOR_REQ,DEV=PI_CAMERA,SUB_DEV=TIMELAPSE,CMD=CAPTURE,SIZE=' + message_size_text + ',VFLIP=' + flip_text + ',FILE_PRE=' + image_file_prefix + ',DELAY=' + frame_delay_text + ',FRAMES=' + num_frames_text + ',SENSOR_REQ_END'
      self.cameraStatusLineEdit.setText("BUSY")
      self.send_camera_sensor_req(sensor_req_message)

def init_globals():
   global __sub_socket_connected__
   __sub_socket_connected__ = False

def main():
   init_globals()
   app = QtGui.QApplication(sys.argv) 
   form = PiCamUIApp() 
   form.show() 
   app.exec_() 

if __name__ == '__main__': 
   main()        
