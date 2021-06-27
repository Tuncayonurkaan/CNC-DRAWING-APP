# This Python file uses the following encoding: utf-8
import sys
import os
import cv2
from scipy.ndimage.morphology import morphological_laplace
import serial
import numpy 
import serial.tools.list_ports
import winreg
import itertools
import time
import threading
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
from svg_to_gcode.compiler.interfaces import Interface
from svg_to_gcode import TOLERANCES
import math
import warnings
from svg_to_gcode.geometry import Vector
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage,QPixmap,QIcon
from PyQt5.QtWidgets import  QMessageBox, QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile,QSize
from PyQt5 import QtWidgets, uic
from skimage.filters import threshold_local
from svg_to_gcode import formulas

power=1

class Custom_Gcode(Interface):
    
    def __init__(self):
        self.position = None
        self._next_speed = None
        self._current_speed = None
        self.precision = abs(round(math.log(TOLERANCES["operation"], 10)))

    def laser_off(self):
       
        if power < 0 or power > 1:
            raise ValueError(f"{power} is out of bounds. Laser power must be given between 0 and 1. "
                             f"The interface will scale it correctly.")

        return f"M3 S{formulas.linear_map(0, 255, power)};"
       

    def set_laser_power(self, power):
        return f"M5;"

    def set_movement_speed(self, speed):
        self._next_speed = speed
        return ''

    def linear_move(self, x=None, y=None, z=None):

        if self._next_speed is None:
            raise ValueError("Undefined movement speed. Call set_movement_speed before executing movement commands.")

        # Don't do anything if linear move was called without passing a value.
        if x is None and y is None and z is None:
            warnings.warn("linear_move command invoked without arguments.")
            return ''

        # Todo, investigate G0 command and replace movement speeds with G1 (normal speed) and G0 (fast move)
        command = "G1"

        if self._current_speed != self._next_speed:
            self._current_speed = self._next_speed
            command += f" F{self._current_speed}"

        # Move if not 0 and not None
        command += f" X{x:.{self.precision}f}" if x is not None else ''
        command += f" Y{y:.{self.precision}f}" if y is not None else ''
        command += f" Z{z:.{self.precision}f}" if z is not None else ''

        if self.position is not None or (x is not None and y is not None):
            if x is None:
                x = self.position.x

            if y is None:
                y = self.position.y

            self.position = Vector(x, y)

        if False:
            print(f"Move to {x}, {y}, {z}")

        return command + ';'


    def set_absolute_coordinates(self):
        return "G90;"

    def set_relative_coordinates(self):
        return "G91;"

    def dwell(self, milliseconds):
        return f"G4 P{milliseconds}"

    def set_origin_at_position(self):
        self.position = Vector(0, 0)
        return "G92 X0 Y0 Z0;"

    def set_unit(self, unit):
        if unit == "mm":
            return "G21;"

        if unit == "in":
            return "G20;"

        return ''

    def home_axes(self):
        return "G28;"    

class main(QWidget):

    def __init__(self):
        super(main, self).__init__()
        call=uic.loadUi('form.ui',self)
        self.count=0
        
        if(len(ports)!=0):
            for i in ports:
                call.comboBox.addItem(i) 
        else:
          call.comboBox.addItem("Port nicht gefunden")  
       
        
        tau_image = QPixmap("icons/tau.png")
        port_image = QPixmap("icons/port.png")
        photo_image=QPixmap("icons/photo.png")
        cam_image = QIcon("icons/cam.png")
        run_image = QIcon("icons/run.png")
        back_image=QIcon("icons/back.png")
        self.label_tau.setPixmap(tau_image)
        self.label_port.setPixmap(port_image)
        self.label_image.setPixmap(photo_image)
        call.pushButton_photo.setIcon(cam_image)
        call.pushButton_Back.setIcon(back_image)
        call.pushButton_take2.setIcon(cam_image)
        call.pushButton_run.setIcon(run_image)
        size = QSize(100, 100)
        size1 = QSize(60, 60)
        call.pushButton_photo.setIconSize(size)
        call.pushButton_run.setIconSize(size1)
        call.pushButton_Back.setIconSize(size1)
        call.pushButton_take2.setIconSize(size)
        call.label_warning.setVisible(False)
        call.pushButton_photo.clicked.connect(self.camClicked)      #Click the camera button and the camera will be activated.
        call.pushButton_take2.clicked.connect(self.takeClicked)
        call.pushButton_Back.clicked.connect(self.backClicked)
        call.pushButton_run.clicked.connect(self.runClicked)
        self.imgLabel.setVisible(False)
        self.imgLabel_2.setVisible(False)
        self.label.setVisible(False)
        self.label2.setVisible(False)
        self.pushButton_Back.setVisible(False)
        self.pushButton_take2.setVisible(False)
        self.pushButton_take2.setVisible(False)
        self.progressBar.setVisible(False)

    def camClicked(self):
        self.logic=0
        self.label.setVisible(True)
        self.label2.setVisible(True)
        self.comboBox.setVisible(False)
        self.pushButton_photo.setVisible(False)
        self.pushButton_run.setVisible(False)
        self.pushButton_take.setVisible(False)
        self.pushButton_run1.setVisible(False)
        self.imgLabel.setVisible(True)
        self.imgLabel_2.setVisible(True)
        self.pushButton_Back.setVisible(True)
        self.pushButton_take2.setVisible(True)
        cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        while True: 
            ret, img = cam.read()
            #---------------------------------------BGA-----------------------------------------------
            resized_image = cv2.resize(img, (260, 200))
            self.displayImage(resized_image,0,1)

#Grayscale
            gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
#Noise reduction (with Gaussian filter)
            blur = cv2.GaussianBlur(gray,(5,5),0)
#Threshold
            warped = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            T = threshold_local(warped, 11, offset = 3, method = "gaussian")
            warped = (warped > T).astype("uint8") * 255
            kernel = numpy.ones((2, 2), numpy.uint8)
            warped = cv2.morphologyEx(warped, cv2.MORPH_CLOSE, kernel)
            cnt, hierarchy = cv2.findContours(warped, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            height, width = resized_image.shape[:2]
            #Canny edge detection
            canny=cv2.Canny(warped,100,200)
            kernel = numpy.ones((5,5),numpy.uint8)
            canny = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
            cnt, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            height,width=resized_image.shape[:2]
            #------------------------------------------BGA----------------------------
            self.displayImage(warped,1,1)
            cv2.waitKey()
            if not ret:
                break
            k=cv2.waitKey(1)
            if self.logic==2:
                break
                
            if self.logic==1:
                self.count +=1
                file='Image/img'+str(self.count)+'.jpg'
                cv2.imwrite(file, warped)
                thread_svg=threading.Thread(target=self.convert_contours_to_svg,args=(cnt,width,height),daemon=True)
                thread_svg.start()
                self.logic=3
                break
        cam.release() 
        for i in range(1,10):
            cv2.destroyAllWindows()
            cv2.waitKey(1)
        self.comboBox.setVisible(True)
        self.pushButton_photo.setVisible(True)
        self.pushButton_run.setVisible(True)
        self.pushButton_take.setVisible(True)
        self.pushButton_run1.setVisible(True)
        self.imgLabel.setVisible(False)
        self.imgLabel_2.setVisible(False)
        self.pushButton_Back.setVisible(False)
        self.pushButton_take2.setVisible(False)
        self.label.setVisible(False)
        self.label2.setVisible(False)
        self.logic=0
        if(self.count!=0):
            image=QPixmap('Image/img'+str(self.count)+'.jpg')   #reads the picture and displays it in the interface
            self.label_image.setPixmap(image)

    def convert_contours_to_svg(self, contours, width, height, to_gcode=True):
        svg = '<svg width="' + str(width) + '" height="' + str(height) + '" xmlns="http://www.w3.org/2000/svg">'
        for c in contours:
            svg += '<path d="M'
            for i in range(len(c)):
                x, y = c[i][0]
                svg += str(x)+ " " + str(y) + " "
            svg += '" style="stroke:black"/>'
        svg += "</svg>"
        with open("Svg/path.svg", "w+") as f:
            f.write(svg)
        if not to_gcode:
            return
        self.convert_svg_to_gcode(svg, 0.3)
        return

    def convert_svg_to_gcode(self, svg, tolerance):
        TOLERANCES['approximation'] = 0.01
        gcode_compiler = Compiler(Custom_Gcode, movement_speed=50000, cutting_speed=40000, pass_depth=5)
        curves = parse_file("Svg/path.svg")
        gcode_compiler.append_curves(curves)
        gcode_compiler.compile_to_file("gcode/path.gcode", passes=1)
        with open("gcode/path.gcode", "ab") as f:
            return_home = b"\nG21G90 G0Z5;\nG90 G0 X0 Y0;\nG90 G0 Z0;"
            f.write(return_home)
        return

    def displayImage(self,img,control,window=1):                 #displays video on camera
        qformat=QImage.Format_Indexed8

        if len(img.shape)==3:
            if(img.shape[2])==4:
                qformat=QImage.Format_RGBA8888

            else:
                qformat=QImage.Format_RGB888

        img=QImage(img,img.shape[1],img.shape[0],qformat)
        img=img.rgbSwapped()
        if control==0:
             self.imgLabel.setPixmap(QPixmap.fromImage(img))                                    
             self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        if control==1:
            self.imgLabel_2.setPixmap(QPixmap.fromImage(img))                                    
            self.imgLabel_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    
    def gcode_to_arduino(self):
         self.progressBar.setVisible(True)
         selected_port=self.comboBox.currentText()
         s = serial.Serial(self.comboBox.currentText(),115200)
         f = open('gcode/path.gcode','r')
         time.sleep(2)   # Wait for Printrbot to initialize
         s.flushInput()  # Flush startup text in serial input
         for j,line in enumerate(f):
           pass
         j+=1
         f.seek(0) 
# Stream g-code
         for index,line in enumerate(f):
           if line.find(';')==-1:
               l=line
           else:
               l=line[:line.index(';')]
           l=l.strip()
           if  (l.isspace()==False and len(l)>0) :
              s.write((l + '\n').encode()) # Send g-code block    
              grbl_out = s.readline() # Wait for response with carriage return
# Wait here until printing is finished to close serial port and file.         
           self.progressBar.setValue(((index+1)*100)/j)
# Close file and serial port     
         self.progressBar.setVisible(False)
         self.label_warning.setText("Ihre Transaktion war erfolgreich!")
         time.sleep(2)
         self.progressBar.setValue(0)
         self.label_warning.setText("Ihre Transaktion läuft, bitte warten Sie ...")
         self.label_warning.setVisible(False)
         self.pushButton_photo.setVisible(True)      
         self.pushButton_run.setVisible(True) 
         self.pushButton_run1.setVisible(True)
         self.pushButton_take.setVisible(True)  
         self.comboBox.setVisible(True) 
         self.label_serial.setVisible(True) 
         f.close()
         s.close()

    def show_popup(self,a):
        if(a==1):
         msg=QMessageBox()
         msg.setWindowTitle("G-Code-Sendevorgang") 
         msg.setIcon(QMessageBox.Question)
         msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
         msg.setText("Bitte geben Sie Ihre Zustimmung zur Durchführung Ihrer Transaktion.")
         msg.setDefaultButton(QMessageBox.Yes)
         result=msg.exec_()

        
        if result == QMessageBox.Yes and len(ports)==0:
          self.portControl=0
          msg2=QMessageBox()
          msg2.setWindowTitle("G-Code-Sendevorgang") 
          msg2.setText("Port nicht gefunden!")
          msg2.setIcon(QMessageBox.Information)
          msg2.exec_()
        if result == QMessageBox.Yes and len(ports)!=0:
          self.portControl=1

          self.pushButton_photo.setVisible(False)     
          self.pushButton_take2.setVisible(False) 
          self.pushButton_Back.setVisible(False) 
          self.pushButton_run.setVisible(False) 
          self.pushButton_run1.setVisible(False)
          self.pushButton_take.setVisible(False)  
          self.comboBox.setVisible(False) 
          self.label_serial.setVisible(False) 


          self.progressBar.setVisible(True)
          self.label_warning.setVisible(True)
          
          
        if result == QMessageBox.No:
          self.portControl=0
          msg.close()
        
    def takeClicked(self):
        self.logic=1

    def backClicked(self):
        self.logic=2

    def runClicked(self):
        self.show_popup(1)
        if(self.portControl==1 and len(ports)!=0):
            thread_svg=threading.Thread(target=self.gcode_to_arduino,daemon=True)
            thread_svg.start()

def serial_ports() -> list:
    path = 'HARDWARE\DEVICEMAP\SERIALCOMM'
    #print(os.path.exists(path))
    ports = []
    #if(os.path.exists(path)):
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    
    for i in itertools.count():
        try:
            ports.append(winreg.EnumValue(key, i)[1])
        except EnvironmentError:
            break
        
    return ports

if __name__ == "__main__":
    app = QApplication([])
    ports = serial_ports()
    widget = main()
    widget.show()
    sys.exit(app.exec_())
