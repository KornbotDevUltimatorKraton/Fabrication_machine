#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author:Chanapai Chuadchum
#Project:Auracore color controller GUI 
#release date:25/2/2020
from PyQt5 import QtCore, QtWidgets, uic,Qt,QtGui 
from PyQt5.QtWidgets import QApplication,QTreeView,QDirModel,QFileSystemModel,QVBoxLayout, QTreeWidget,QStyledItemDelegate, QTreeWidgetItem,QLabel,QGridLayout,QLineEdit,QDial,QTreeWidget, QTreeWidgetItem, QApplication,QWidget,QTabWidget,QComboBox
from PyQt5.QtGui import QPixmap,QIcon,QImage,QPalette,QBrush
from pyqtgraph.Qt import QtCore, QtGui   #PyQt graph to control the model grphic loaded  
import pyqtgraph.opengl as gl
from qtpy import QtWidgets
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor, MainWindow
import csv 
import os 
import sys 
import cv2 
import pyfirmata  #Pyfirmata for serial protocol 
seriallist  = os.listdir("/sys/class/tty") #Getting the serial list directory
serialmem = []
serialmem1 = [] 
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,parent=None,show=True, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
    
        QtWidgets.QMainWindow.__init__(self, parent)
        QWidget.__init__(self)
        #Load the UI Page
        self.setWindowIcon(QtGui.QIcon('/home/kornbotdev/Fab_machine/apple-touch-icon.png'))
        # set the title
        self.setWindowTitle("Icon")
  
        # setting  the geometry of window
        self.setGeometry(0, 0, 400, 300)
        uic.loadUi('Fabrication_machine.ui', self)
        self.setWindowTitle('Fabrication Machine')
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.darkGray)
        self.setPalette(p)
        #oImage = QImage("NeuralFuture.jpeg")
        #sImage = oImage.scaled(QSize(300,200))                   # resize Image to widgets size
        palette = QPalette()
        #palette.setBrush(QPalette.Window, QBrush(oImage))
        #self.setPalette(palette)
       
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.
           # Dial set control rotation degree of the pick and place for settings 
        self.dial.setMinimum(0)
        self.dial.setMaximum(180)
        self.dial.setValue(0) # Set the value at the 0 
        self.dial.valueChanged.connect(self.Rot_motion)
           #Dial set control the uv light intensity  
        self.dial_3.setMinimum(0)
        self.dial_3.setMaximum(10) #Light control by microcontroller onboard of the robotics arm for the fabrication machine  
        self.dial_3.setValue(0) # Set the value at the 0 
        self.dial_3.valueChanged.connect(self.UV_intensity)  
           #Dial set control for the etching process function 
        self.dial_2.setMinimum(0)
        self.dial_2.setMaximum(10) #Light control by microcontroller onboard of the robotics arm for the fabrication machine  
        self.dial_2.setValue(0) # Set the value at the 0 
        self.dial_2.valueChanged.connect(self.Etching_timing)  
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
           # X-axis slider function 
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.valueChanged.connect(self.X_axis_slider)
        #self.textEdit_5.setText(str(DataInit[4]))
           # Y-axis slider function 
        self.horizontalSlider_2.setMinimum(0)
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setValue(0)
        self.horizontalSlider_2.valueChanged.connect(self.Y_axis_slider)
           #Z-axis slider function 
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setValue(0)
        self.verticalSlider.valueChanged.connect(self.Z_axis_slider)
        
        #combobox 1 
        self.comboBox = QComboBox(self) #Getting the combobox function to work 
        self.comboBox.addItem("Non-serial")
        for i in range(0,len(seriallist)):
              if len(str(seriallist[i]).split("USB")) >= 2:
                        serialmem.append(str(seriallist[i])) 
              if len(str(seriallist[i]).split("ACM")) >=2:
                        serialmem.append(str(seriallist[i])) 
        self.comboBox.addItems(serialmem)   #Add list of serial port 
        self.comboBox.activated[str].connect(self.Serialfunc)      
        self.comboBox.move(60, 810)
        #Combobox 2 
        self.comboBox_2 = QComboBox(self) #Getting the combobox function to work 
        self.comboBox_2.addItem("Non-serial")
        for i in range(0,len(seriallist)):
              if len(str(seriallist[i]).split("USB")) >= 2:
                        serialmem1.append(str(seriallist[i])) 
              if len(str(seriallist[i]).split("ACM")) >=2:
                        serialmem1.append(str(seriallist[i])) 
        self.comboBox_2.addItems(serialmem1)   #Add list of serial port 
        self.comboBox_2.activated[str].connect(self.Serialfunc2)      
        self.comboBox_2.move(60, 850)
    def Rot_motion(self): 
        print("Degree rotation:= %i\tdegree" % (self.dial.value())) # getting the number to calculate to degree rotation of the pick and place machine 
        self.lcdNumber_6.display(self.dial.value())
        self.lcdNumber_6.setStyleSheet("""QLCDNumber { background-color: black; }""")

    def UV_intensity(self): 
        print("UV light intensity:= %f" % (self.dial_3.value()))   
        print("PWM_output:=%f\tpercentage" %(0.1*self.dial_3.value()))
        self.lcdNumber_4.display(10*self.dial_3.value())
        self.lcdNumber_4.setStyleSheet("""QLCDNumber { background-color: black; }""")
    def Etching_timing(self):
        print("Etching_timing:= %f" %(self.dial_2.value()))
        print("Time_output:=%f\tms" %(0.2*self.dial_2.value()))
        self.lcdNumber_5.display(0.2*self.dial_2.value())
        self.lcdNumber_5.setStyleSheet("""QLCDNumber { background-color: black; }""")
    def X_axis_slider(self):
        print("X_axis:= %f" %(self.horizontalSlider.value()))
        self.lcdNumber.display(self.horizontalSlider.value()) # Processing timing 
        self.lcdNumber.setStyleSheet("""QLCDNumber { background-color: black; }""")
    def Y_axis_slider(self):
        print("Y_axis:= %f" %(self.horizontalSlider_2.value()))
        self.lcdNumber_2.display(self.horizontalSlider_2.value()) # Processing timing 
        self.lcdNumber_2.setStyleSheet("""QLCDNumber { background-color: black;}""")
    def Z_axis_slider(self):
        print("Z_axis:= %f" %(self.verticalSlider.value()))
        self.lcdNumber_3.display(self.verticalSlider.value()) # Processing timing 
        self.lcdNumber_3.setStyleSheet("""QLCDNumber { background-color: black;}""")
    def Serialfunc(self,text):
              print("serial_selected",text)
    def Serialfunc2(self,text2):
              print("serial_selected",text2)
class Compoent_id_position(QWidget):
        def __init__(self):
            super().__init__() 
            self.w = QWidget() 
            self.w.resize(351,951)
            l1 = QTreeWidgetItem(["String A", "String B", "String C"])
            l2 = QTreeWidgetItem(["String AA", "String BB", "String CC"])

            for i in range(3):
               l1_child = QTreeWidgetItem(["Child A" + str(i), "Child B" + str(i), "Child C" + str(i)])
               l1.addChild(l1_child)

            for j in range(2):
                l2_child = QTreeWidgetItem(["Child AA" + str(j), "Child BB" + str(j), "Child CC" + str(j)])
                l2.addChild(l2_child)
            self.treeWidget = QTreeWidget(self.w)
            self.treeWidget.resize(351, 951)
            self.treeWidget.setColumnCount(3)
            self.treeWidget.setHeaderLabels(["Components", "ID", "Positioning"])
            self.treeWidget.addTopLevelItem(l1)
            self.treeWidget.addTopLevelItem(l2)
            self.tab_2 = QWidget()
            self.tab_2.layout.addWidget(self.treeWidget)
            self.tab_2.setLayout(self.tab_2.layout)
            #self.tab_2.addTab(Compoent_id_position(), "Realtime process structures")

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()

    main.show()
    sys.exit(app.exec_())

    
if __name__ == '__main__':         
    main()
