#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os.path
import sys
import argparse
from __init__ import VERSION, DEFAULTDEVICE, PORT, CALLSIGN
from epicmon import epicMon, epicData
from datetime import datetime
USAGE = \
"""
epicmonserverhttp
"""

DESCRIPTION = \
"""
epicmonserver - A utility to monitor and display status of a West Mountain Radio Epic Power Gate via HTTP.
"""

EPILOG = \
"""
That is all!
"""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if (self.path == '/') or (self.path == '/getstatus'):
            #if args.deviceName:
            pgate = epicMon(DEFAULTDEVICE)
            if pgate:
                gateStat = epicData(pgate.get_status())
                self.ShowHTML(gateStat)
                #gateStat.showValues()
        elif self.path == '/exit':
            print('Server exiting... bye!')
            exit()

    def ShowHTML(self, dataList):
        htdoc = """<!DOCTYPE html>
                    <html>
                    <head>
                    <title>{}  Mobile Power Status</title>
                    <meta http-equiv="refresh" content="60">
                    </head>
                    <body>
                    <h1 align='center'>{}  Mobile Power Status</h1>
                    <p align='center'>{}</p>
                    <hr>""".format(CALLSIGN, CALLSIGN, datetime.now())
        #for l in dataList:
        htdoc += '<p>{}<br>{}</p>'.format(dataList.deviceStg, 
                                          dataList.configStg)
        htdoc += """<p>Vehicle Battery Voltage: {} V<br>
                       Charge State: {}<br>
                       Time in current state: {} minutes<br>
                       Rack Battery Voltage: {} V<br>
                       Current: {} A<br>
                       Solar Volts: {} V<br>
                       Rack Battery Temperature: {} F
                 </p>""".format(dataList.psVolts,
                                dataList.battState,
                                dataList.inStateTime,
                                dataList.battVolts,
                                dataList.battAmps,
                                dataList.solarVolts,
                                dataList.pgateTemp)
        htdoc += "<p>Raw Data:<br>{}<br>\n".format(dataList.rawStatus[8])
        htdoc += "{}<br></p>\n".format(dataList.rawStatus[9])

        htdoc += """</body>
                </html>"""
        self.wfile.write(htdoc.encode('utf-8'))

def parseMyArgs():
    parser = argparse.ArgumentParser(\
                    description = DESCRIPTION, usage = USAGE)
    parser.add_argument('-v', '--version', 
                        action='version', 
                        version = VERSION)

    parser.add_argument('-c', '--callSign',
                                   default = CALLSIGN,
            help="""Call sign used for HTML display.
                    default is {}""".format(CALLSIGN))

    parser.add_argument('-d', '--deviceName',
                                   default = DEFAULTDEVICE,
            help="""Use deviceName as serial input device.
                    default is {}""".format(DEFAULTDEVICE))

    parser.add_argument('-p', '--Port', type=int,
                                   default = PORT,
            help="""Use Port as network port for connection.
                    default is {}""".format(PORT))

    parser.add_argument('-t', '--epicMonTerm',
                    default =  None,
            help="""Display raw status N lines of output from 
                    the Epic PowerGate and quit. Entering a value
                    of 0 will cause the stream to run indefinately.
                    """)

    parser.add_argument('-V', '--epicVersion',
                    default =  False,
                    action = 'store_true',
            help="""Read and report the Epic PowerGate verison.""")

    args = parser.parse_args()
    return args

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print("Starting server on port {}...".format(PORT))
    httpd.serve_forever()



if __name__ == '__main__':
    args = parseMyArgs()
    if args.deviceName:
        DEFAULTDEVICE = args.deviceName
    if args.callSign:
        CALLSIGN = args.callSign
    if args.Port:
        PORT = args.Port
    run()
