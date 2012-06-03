#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/

QT Port of the VB.NET Example for the Phidgets InterfaceKit example program.

"""
import sys, os
from PyQt4 import QtGui, QtCore
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, \
    ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit
from resources import GUI


class GUIWindow(QtGui.QWidget, GUI.Ui_Form):
    def __init__(self, parent=None):
        super(GUIWindow, self).__init__(parent)
        
        self.setupUi(self)
        self.resize(780, 400)
        self.setWindowTitle("QInterfaceKit - PyQT4 Phidgets Interface Kit")
        iconfile = os.path.join(os.path.abspath(os.getcwd()), 
                                os.path.join("resources", "icon.png"))
        self.setWindowIcon(QtGui.QIcon(iconfile))
        
        self.digiInArray = []
        self.digiOutArray = []
        self.analogInArray = []
        
        self.makeDigiInArray()
        self.makeDigiOutArray()
        self.makeAnalogInArray()
        
        self.sliderSensitivity.setValue(0)
        self.sliderSensitivity.setEnabled(False)
        
        self.checkBoxRatiometric.setEnabled(False)
        self.checkBoxRatiometric.setChecked(False)
        
        self.connect(self.sliderSensitivity,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.sensitivitySliderChangedSlot)

        self.connect(self.sliderSensitivity,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.lcdSensitivity,
                     QtCore.SLOT("display(int)"))
        
    def outputLog(self, QString):
        self.textEditOutputLog.append("%s" % QString)
    
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, "Message", 
                         quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    #===========================================================================
    # Define slots for interfacekit events
    #===========================================================================
    def interfaceKitAttachedSlot(self, event):
        interfaceKit = event.device
        self.lineEditAttached.setText("%s" % interfaceKit.isAttached())
        self.lineEditName.setText("%s" % interfaceKit.getDeviceName())
        self.lineEditSerial.setText("%s" % interfaceKit.getSerialNum())
        self.lineEditVersion.setText("%s" % interfaceKit.getDeviceVersion())
        self.lineEditDigiInput.setText("%i" % interfaceKit.getInputCount())
        self.lineEditDigiOutput.setText("%i" % interfaceKit.getOutputCount())
        self.lineEditAnalogInput.setText("%i" % interfaceKit.getSensorCount())
        
        for i in range(interfaceKit.getInputCount()):
            self.digiInArray[i].show()
        
        for i in range(interfaceKit.getOutputCount()):
            self.digiOutArray[i].show()
            self.digiOutArray[i].setEnabled(True)
            
        for i in range(interfaceKit.getSensorCount()):
            self.analogInArray[i].show()
            
        if interfaceKit.getSensorCount() > 0:
            self.sliderSensitivity.setEnabled(True)
            self.sliderSensitivity.setRange(0, 1000)
            self.sliderSensitivity.setValue(interfaceKit.getSensorChangeTrigger(0))
            
            interfaceKit.setRatiometric(True)
            
            self.checkBoxRatiometric.setEnabled(True)
            self.checkBoxRatiometric.setChecked(interfaceKit.getRatiometric())
        
        self.outputLog(QtCore.QString("Attached %s (serial: %i)" \
                                      % (interfaceKit.getDeviceName(),
                                        interfaceKit.getSerialNum())))


    def interfaceKitDetachedSlot(self, event):
        interfaceKit = event.device
        self.lineEditAttached.setText("%s" % interfaceKit.isAttached())
        self.lineEditName.setText("")
        self.lineEditSerial.setText("")
        self.lineEditVersion.setText("")
        self.lineEditDigiInput.setText("")
        self.lineEditDigiOutput.setText("")
        self.lineEditAnalogInput.setText("")
        
        for i in range(16):
            self.digiInArray[i].setChecked(False)
            self.digiInArray[i].hide()

        for i in range(16):
            self.digiOutArray[i].setChecked(False)
            self.digiOutArray[i].setEnabled(False)
            self.digiOutArray[i].hide()
            
        for i in range(8):
            self.analogInArray[i].setText("")
            self.analogInArray[i].hide()
            
        self.sliderSensitivity.setValue(0)
        self.sliderSensitivity.setEnabled(False)
        
        self.checkBoxRatiometric.setChecked(False)
        self.checkBoxRatiometric.setEnabled(False)
        
        self.outputLog(QtCore.QString("InterfaceKit detached"))


    def interfaceKitErrorSlot(self, event):
        interfaceKit = event.device
        QtGui.QMessageBox.critical(self,
                                   "Error",
                                   "%i: %s" % (event.eCode, event.description),
                                   QtGui.QMessageBox.Ok, QtGui.QMessageBox.Abort)
        self.outputLog(QtCore.QString("%s (serial: %i) Phidget Error %i: %s" % \
                                      (interfaceKit.getDeviceName(),
                                       interfaceKit.getSerialNum(),
                                       event.eCode(),
                                       event.description)))
        
    def interfaceKitInputChangedSlot(self, event):
        interfaceKit = event.device
        if event.state:
            self.digiInArray[event.index].setChecked = event.value
            
        self.outputLog(QtCore.QString("%s: Input %i: %s" % \
                                      (interfaceKit.getDeviceName(),
                                       event.index, event.state)))
        
    def interfaceKitOutputChangedSlot(self, event):
        interfaceKit = event.device
        if event.state:
            self.digiInArray[event.index].setChecked = event.value
            
        self.outputLog(QtCore.QString("%s: Output %i: %s" % \
                                      (interfaceKit.getDeviceName(),
                                       event.index, event.state)))
        
    def interfaceKitSensorChangedSlot(self, event):
        interfaceKit = event.device
        self.analogInArray[event.index].setText(("%i" % event.value))
        self.outputLog(QtCore.QString("%s: Sensor %i: %i" % \
                                      (interfaceKit.getDeviceName(),
                                       event.index, event.value)))
        
    def sensitivitySliderChangedSlot(self, value):
        self.emit(QtCore.SIGNAL("sensitivityChanged"), value)
        
    
    #===========================================================================
    # Initialize GUI
    #===========================================================================
    def makeDigiInArray(self):
        self.digiInArray.append(self.checkBox0)
        self.digiInArray.append(self.checkBox1)
        self.digiInArray.append(self.checkBox2)
        self.digiInArray.append(self.checkBox3)
        self.digiInArray.append(self.checkBox4)
        self.digiInArray.append(self.checkBox5)
        self.digiInArray.append(self.checkBox6)
        self.digiInArray.append(self.checkBox7)
        self.digiInArray.append(self.checkBox8)
        self.digiInArray.append(self.checkBox9)
        self.digiInArray.append(self.checkBox10)
        self.digiInArray.append(self.checkBox11)
        self.digiInArray.append(self.checkBox12)
        self.digiInArray.append(self.checkBox13)
        self.digiInArray.append(self.checkBox14)
        self.digiInArray.append(self.checkBox15)
        
        for i in range(16):
            self.digiInArray[i].hide()
            
    def makeDigiOutArray(self):
        self.digiOutArray.append(self.checkBox16)
        self.digiOutArray.append(self.checkBox17)
        self.digiOutArray.append(self.checkBox18)
        self.digiOutArray.append(self.checkBox19)
        self.digiOutArray.append(self.checkBox20)
        self.digiOutArray.append(self.checkBox21)
        self.digiOutArray.append(self.checkBox22)
        self.digiOutArray.append(self.checkBox23)
        self.digiOutArray.append(self.checkBox24)
        self.digiOutArray.append(self.checkBox25)
        self.digiOutArray.append(self.checkBox26)
        self.digiOutArray.append(self.checkBox27)
        self.digiOutArray.append(self.checkBox28)
        self.digiOutArray.append(self.checkBox29)
        self.digiOutArray.append(self.checkBox30)
        self.digiOutArray.append(self.checkBox31)
        
        for i in range(16):
            self.digiOutArray[i].hide()
        
    def makeAnalogInArray(self):
        self.analogInArray.append(self.lineEditAnalogIn0)
        self.analogInArray.append(self.lineEditAnalogIn1)
        self.analogInArray.append(self.lineEditAnalogIn2)
        self.analogInArray.append(self.lineEditAnalogIn3)
        self.analogInArray.append(self.lineEditAnalogIn4)
        self.analogInArray.append(self.lineEditAnalogIn5)
        self.analogInArray.append(self.lineEditAnalogIn6)
        self.analogInArray.append(self.lineEditAnalogIn7)
        
        for i in range(8):
            self.analogInArray[i].hide()
        

class PhidgetsEventThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(PhidgetsEventThread, self).__init__(parent)

        try:
            self.interfaceKit = InterfaceKit()
            self.interfaceKit.openPhidget()
            self.interfaceKit.setOnAttachHandler(self.interfaceKitAttachedEvent)
            self.interfaceKit.setOnDetachHandler(self.interfaceKitDetachEvent)
            self.interfaceKit.setOnErrorhandler(self.interfaceKitErrorSlot)
            self.interfaceKit.setOnInputChangeHandler(self.interfaceKitInputChangedEvent)
            self.interfaceKit.setOnOutputChangeHandler(self.interfaceKitOutputChangedEvent)
            self.interfaceKit.setOnSensorChangeHandler(self.interfaceKitSensorChangedEvent)
        except RuntimeError as e:
            print "Runtime Exception: %s" % (e.details)
            print "Exiting..."
            sys.exit(1)
            
        except PhidgetException as e:
            print "Phidget Exception %i: %s" % (e.code, e.details)
            print "Exiting..."
            sys.exit(1) 
    
    
    #===========================================================================
    # On Interfacekit events, emit signals to main thread for updating GUI
    #===========================================================================
    def interfaceKitAttachedEvent(self, event):
        self.emit(QtCore.SIGNAL("interfaceKitAttachedSlot"), event)
    
    def interfaceKitDetachEvent(self, event):
        self.emit(QtCore.SIGNAL("interfaceKitDetachedSlot"), event)
        
    def interfaceKitErrorSlot(self, event):
        self.emit(QtCore.SIGNAL("interfaceKitErrorSlot"), event)
    
    def interfaceKitInputChangedEvent(self, event):
        self.emit(QtCore.SIGNAL("interfaceKitInputChangedSlot"), event)
    
    def interfaceKitOutputChangedEvent(self, event):
        self.emit(QtCore.SIGNAL("interfaceKitOutputChangedSlot"), event)
    
    def interfaceKitSensorChangedEvent(self, event):
        self.emit(QtCore.SIGNAL("interfaceKitSensorChangedSlot"), event)
    
    def setSensorSensitivity(self, value):
        try:
            for i in range(self.interfaceKit.getSensorCount()):
                self.interfaceKit.setSensorChangeTrigger(i, value)
        except PhidgetException as e:
            print "Could not set sensitivity: %s" % e.details
            
    def run(self):
        self.exec_()
        
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = GUIWindow()
    interfaceKitThread = PhidgetsEventThread()
    interfaceKitThread.start()
    window.show()
    
    #===========================================================================
    # Connect signals
    #===========================================================================
    QtCore.QObject.connect(interfaceKitThread,
                           QtCore.SIGNAL("interfaceKitAttachedSlot"),
                           window.interfaceKitAttachedSlot,
                           QtCore.Qt.QueuedConnection)
    
    QtCore.QObject.connect(interfaceKitThread,
                           QtCore.SIGNAL("interfaceKitDetachedSlot"),
                           window.interfaceKitDetachedSlot,
                           QtCore.Qt.QueuedConnection)
    
    QtCore.QObject.connect(interfaceKitThread,
                           QtCore.SIGNAL("interfaceKitErrorSlot"),
                           window.interfaceKitErrorSlot,
                           QtCore.Qt.QueuedConnection)

    QtCore.QObject.connect(interfaceKitThread,
                           QtCore.SIGNAL("interfaceKitInputChangedSlot"),
                           window.interfaceKitInputChangedSlot,
                           QtCore.Qt.QueuedConnection)
    
    QtCore.QObject.connect(interfaceKitThread,
                           QtCore.SIGNAL("interfaceKitOutputChangedSlot"),
                           window.interfaceKitOutputChangedSlot,
                           QtCore.Qt.QueuedConnection)
    
    QtCore.QObject.connect(interfaceKitThread,
                           QtCore.SIGNAL("interfaceKitSensorChangedSlot"),
                           window.interfaceKitSensorChangedSlot,
                           QtCore.Qt.QueuedConnection)
    
    QtCore.QObject.connect(window,
                           QtCore.SIGNAL("sensitivityChanged"),
                           interfaceKitThread.setSensorSensitivity,
                           QtCore.Qt.QueuedConnection)

    # Run main event loop
    sys.exit(app.exec_())
    
    
    
    
    
    