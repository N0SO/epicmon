#!/usr/bin/env python3
from serial import Serial
from epicmon.__init__ import VERSION
from datetime import datetime


class epicData():
    def __init__(self, gdata=None):
        if gdata:
            self.parseGdata(gdata)
        else:
            self.deviceStg = None
            self.configStg = None
            self.battState = None
            self.battVolts = None
            self.battAmps = None
            self.psVolts = None
            self.solarVolts = None
            self.pgateTemp = None

        self.rawStatus =  gdata

    def parseGdata(self, gdata):
        self.deviceStg = gdata[2]
        self.configStg = gdata[3]
        statParts = gdata[8]
        self.battState = statParts[0:10]
        self.battVolts = self.stripData(statParts[21:31])
        self.battAmps = self.stripData(statParts[32:40])
        self.psVolts = self.stripData(statParts[11:20])
        self.solarVolts = self.stripData(statParts[41:53])
        self.pgateTemp = self.stripData(statParts[63:71])
        return True

    def stripData(self, strData):
        temp=''.join(i for i in strData if self.isdigit(i))
        return temp

    def isdigit(self, c):
        if c in('0123456789.'):
            return True
        else:
            return False


    def showValues(self):
        print("""
Device ID:{}
Config string: {}
Charge Status: {}
Power Source Voltage: {} V
Battery Voltage: {} V
Current: {} A
Solar Voltage: {} V
Powergate Temperature: {} F

Raw Data:
{}
{}""".format(self.deviceStg,
             self.configStg,
             self.battState,
             self.psVolts,
             self.battVolts,
             self.battAmps,
             self.solarVolts,
             self.pgateTemp,
             self.rawStatus[8],
             self.rawStatus[9]))


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

    def showStatus(self):
        gdata = epicData(self.get_status())
        gdata.showValues()


