#
# sensor server picam module GUI
#
from PyQt4 import QtGui 
import sys 
import zmq

import PiCamUIDesign 
              
class PiCamUIApp(QtGui.QMainWindow, PiCamUIDesign.Ui_MainWindow):
   def __init__(self):
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
      self.imagePathLineEdit.setText("/home/Pi/Pictures/picam_image001.jpg")
      self.videoPathLineEdit.setText("/home/Pi/Pictures/picam_video001.h264")
      self.timelapsePathLineEdit.setText("/home/Pi/Pictures/timelapse-01-")

      # Pre-populate IP address and ports
      self.ipAddressLineEdit.setText("127.0.0.1")
      self.reqPortLineEdit.setText("5557")
      self.subPortLineEdit.setText("5558")

      # Pre-populate Camera Status
      self.cameraStatusLineEdit.setText("IDLE")

      # Connect buttons
      self.imagePushButton.clicked.connect(self.send_capture_image_message) 
      self.videoPushButton.clicked.connect(self.send_capture_video_message) 
      self.timelapsePushButton.clicked.connect(self.send_capture_timelapse_message) 
      self.ConnectPushButton.clicked.connect(self.connect_to_ports) 
      self.connected = False

      # setup ZMQ context and create socket
      self.context = zmq.Context()
      self.req_socket = self.context.socket(zmq.REQ)
      self.req_socket_connected = False

   def send_camera_sensor_req(self, req_message, ip_addr):
       print 'Sending Message to Address:' + ip_addr
       print req_message
       ip_string = 'tcp://' + ip_addr + ':5557'
       if self.req_socket_connected == False:
           self.req_socket.connect(str(ip_string))
       self.req_socket.send(str(req_message))
       reply_message = self.req_socket.recv()
       print 'Received Pi_Camera sensor reply:' , reply_message

   def connect_to_ports(self):
       if self.connected == False:
          print 'connecting to the ZMQ remote ports!'
          self.connected = True
          self.connectedCheckBox.setChecked(True)
       else:
           print 'already connected to the ports!'

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
      ip_address = self.ipAddressLineEdit.text()
      self.send_camera_sensor_req(sensor_req_message, ip_address)

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
      ip_address = self.ipAddressLineEdit.text()
      self.send_camera_sensor_req(sensor_req_message, ip_address)

 
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
      ip_address = self.ipAddressLineEdit.text()
      self.send_camera_sensor_req(sensor_req_message, ip_address)


def main():
   app = QtGui.QApplication(sys.argv) 
   form = PiCamUIApp() 
   form.show() 
   app.exec_() 

if __name__ == '__main__': 
   main()        
