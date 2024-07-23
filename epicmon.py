#!/usr/bin/env python3
from serial import Serial
from epicmon.__init__ import VERSION
from datetime import datetime

class epicMon():
    def __init__(self, devicename = None):
        self.deviceName = devicename

        if devicename:
            self.serialCon = self.openDevice(devicename)
        else:
            self.serialCon = None

    def openDevice(self,  serialport):
        try:
            ser = Serial(serialport)
        except:
            print('Error opening serial port {}'.format(serialport))
            ser = None
        return ser

    def readPort(self):
        return self.serialCon.readline().decode().rstrip()

    def readBytes(self):
        """Read and return byte arry"""
        return self.serialCon.readline()

    def getEpicVersion(self):
        status = None
        if self.serialCon:
           status=list()
           self.serialCon.write(b'\n')
           for i in range(4):
               st = self.readPort()
               if i >  1:
                   status.append(st)
        return status

    def get_status(self, loops=10):
        retBuf = []
        self.serialCon.write(b'\n')
        for i in range(loops):
            retBuf.append(self.readPort())
        return retBuf

    def epicMonTerm(self, loops=None):
        self.serialCon.write(b'\n')
        if loops != '0':
            for i in range(int(loops)):
               print(self.readPort())
        else:
            while 1:
               print(self.readPort())

