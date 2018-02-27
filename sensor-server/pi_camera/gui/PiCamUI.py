#
# sensor server picam module GUI
#
from PyQt4 import QtGui 
import sys 

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

      # Pre-populate IP address
      self.ipAddressLineEdit.setText("127.0.0.1")

      # Pre-populate Camera Status
      self.cameraStatusLineEdit.setText("IDLE")

      # Connect buttons
      self.imagePushButton.clicked.connect(self.send_capture_image_message) 
      self.videoPushButton.clicked.connect(self.send_capture_video_message) 
      self.timelapsePushButton.clicked.connect(self.send_capture_timelapse_message) 


   def send_capture_image_message(self):
      print 'Send a capture image message!'                       
      image_size_text = self.imageSizeComboBox.currentText()
      print '  size --> ',image_size_text
      image_file_name = self.imagePathLineEdit.text()
      print '  file --> ',image_file_name
      if self.imageCheckBox.isChecked() == True:
          flip_image = True
          print '  Flip image '
      else:
          flip_image = False
          print '  Do not flip image'
      ip_address = self.ipAddressLineEdit.text()
      print '  send message to : ',ip_address


   def send_capture_video_message(self):
      print 'Send a capture video message!'                       
      video_size_text = self.videoSizeComboBox.currentText()
      print '  size --> ',video_size_text
      video_file_name = self.videoPathLineEdit.text()
      print '  file --> ',video_file_name
      if self.videoCheckBox.isChecked() == True:
          flip_video = True
          print '  Flip Video '
      else:
          flip_video = False
          print '  Do not flip Video'
      video_seconds = self.videoLengthSpinBox.value()
      print '  video length in seconds --> ',video_seconds

      ip_address = self.ipAddressLineEdit.text()
      print '  send message to : ',ip_address

 
   def send_capture_timelapse_message(self):
      print 'Send a capture timelapse message!'                       
      image_size_text = self.timelapseSizeComboBox.currentText()
      print '  size --> ',image_size_text
      image_file_prefix = self.timelapsePathLineEdit.text()
      print '  file prefix --> ', image_file_prefix
      if self.timelapseCheckBox.isChecked() == True:
          flip_image = True
          print '  Flip image '
      else:
          flip_image = False
          print '  Do not flip image'
      number_of_frames = self.timelapseFramesSpinBox.value()
      print '  number of frames --> ', number_of_frames
      frame_delay = self.timelapseDelaySpinBox.value()
      print '  delay between frames --> ', frame_delay
      ip_address = self.ipAddressLineEdit.text()
      print '  send message to : ',ip_address


def main():
   app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
   form = PiCamUIApp()                 # We set the form to be our ExampleApp (design)
   form.show()                         # Show the form
   app.exec_()                         # and execute the app

if __name__ == '__main__':             # if we're running file directly and not importing it
   main()                              # run the main function
