#!/usr/bin/env python3
from serial import Serial
from __init__ import VERSION
from datetime import datetime
import re,  subprocess

class epicData():
    def __init__(self, gdata=None):
        if gdata:
            self.parseGdata(gdata)
        else:
            self.deviceStg = None
            self.configStg = None
            self.battState = None
            self.inStateTime = None
            self.battVolts = None
            self.battAmps = None
            self.psVolts = None
            self.solarVolts = None
            self.pgateTemp = None

        self.cpuTemp = None
        self.rawStatus =  gdata
 
    def _parsegatestg(self,gdata):
        retdata = None
        if ( (gdata != None) and (len(gdata) >0) ):
            gdata = gdata.strip()
            partstg = gdata.split('  ')
            #print(f'string data = {gdata}\nstring parts = {partstg} len={len(partstg)}')
            if len(partstg) >= 7 :
                """
                They really goon up this string and make it hard to parse!
                If the string length > 7 skip the [1] element.
                """
                if len(partstg) >=8 :
                    fixedstg = []
                    for i in range(len(partstg)):
                        if i != 1:
                            fixedstg.append(partstg[i])
                    partstg = fixedstg
                    #print (f'Fixed partstg = {partstg}')
                self.battState = partstg[0].strip()
                self.inStateTime = self.stripData(partstg[4])
                vparts = partstg[1].strip().split(' ')
                #print(f'vparts = {vparts}')
                if (len(vparts)>=2):
                   self.battVolts = self.stripData(vparts[2])
                   self.psVolts = self.stripData(vparts[1])
                self.battAmps = self.stripData(partstg[2])
                self.solarVolts = self.stripData(partstg[3])
                self.pgateTemp = self.stripData(partstg[5])
        return retdata
        
    def parseGdata(self, gdata):
        #print(gdata)
        self.deviceStg = gdata[2]
        self.configStg = gdata[3]
        statParts = gdata[8]
        parts = self._parsegatestg(statParts)
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
Charge State: {}
Time in current state: {} Minutes
Vehicle Battery Voltage: {} V
Rack Battery Voltage: {} V
Current: {} A
Solar Voltage: {} V
Rack Battery Temperature: {} F
Host CPU Temperature: {} C
Raw Data:
{}
{}""".format(self.deviceStg,
             self.configStg,
             self.battState,
             self.inStateTime,
             self.psVolts,
             self.battVolts,
             self.battAmps,
             self.solarVolts,
             self.pgateTemp,
             self.cpuTemp,
             self.rawStatus[8],
             self.rawStatus[9]))

    def displayNR(self):
        print(\
"""
Charge State: {}
Time in current state: {} minutes
Vehicle Battery Voltage: {} V
Battery Voltage: {} V
Current: {} A
Rack Battery Temperature: {} F
Host CPU Temperature: {} C
""".format( self.battState,
            self.inStateTime,
            self.psVolts,
            self.battVolts,
            self.battAmps,
            self.pgateTemp,
            self.cpuTemp))

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
        #retBuf.append(self.getcpuTemp()[0])
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
        gdata.cpuTemp = self.getcpuTemp()[0]
        gdata.showValues()

    def showNR(self):
        """
        Show status for Node Red display.
        """
        gdata = epicData(self.get_status())
        gdata.cpuTemp = self.getcpuTemp()[0]
        gdata.displayNR()

    def getcpuTemp(self):
        temp = None
        err, msg = subprocess.getstatusoutput('vcgencmd measure_temp')
        if not err:
            m = re.search(r'-?\d\.?\d*', msg)   # a solution with a  regex
            try:
                temp = float(m.group())
            except ValueError: # catch only error needed
                pass
        return temp, msg

