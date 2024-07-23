#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os.path
import sys
import argparse

whereami = os.path.split( os.path.realpath(__file__) )
pathsplit = os.path.split(whereami[0])
#print("here I am :", whereami, pathsplit)

DEVMODPATH = [pathsplit[0],'/home/mike/Projects']
#print('Using DEVMODPATH=',DEVMODPATH)
#os.chdir(pathsplit[0])

for mypath in DEVMODPATH:
        if ( os.path.exists(mypath) and \
          (os.path.isfile(mypath) == False) ):
            sys.path.insert(0, mypath)

from epicmon.__init__ import VERSION, DEFAULTDEVICE
from epicmon.epicmon import epicMon
from datetime import datetime
PORT = 50007
USAGE = \
"""
epicmon
"""

DESCRIPTION = \
"""
epicmon - A utility to monitor and display status of a West Mountain Radio Epic Power Gate.
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
        #print("Bite me world!\n\n{},      {}".format(self.path, self.requestline))
        #self.wfile.write(b"Hello, World!")
        if self.path == '/exit':
            print('Server exiting... bye!')
            exit()
        elif self.path == '/bite':
            print('Bite me!')
        elif self.path == '/getstatus':
            #if args.deviceName:
            pgate = epicMon(DEFAULTDEVICE)
            if pgate:
                gateStat = pgate.get_status(10)
                self.ShowHTML(gateStat)

    def ShowHTML(self, dataList):
        htdoc = b"""<!DOCTYPE html>
                    <html>
                    <body>
                    <h1>N0SO Mobile Power Status</h1>
                    <hr>"""
        #for l in dataList:
        htdoc += "{}<br>\n".format(dataList[8]).encode('utf-8')
        htdoc += "{}<br>\n".format(dataList[9]).encode('utf-8')

        htdoc += b"""</body>
                </html>"""
        self.wfile.write(htdoc)


def parseMyArgs():
    parser = argparse.ArgumentParser(\
                    description = DESCRIPTION, usage = USAGE)
    parser.add_argument('-v', '--version', 
                        action='version', 
                        version = VERSION)

    parser.add_argument('-d', '--deviceName',
                                   default = DEFAULTDEVICE,
            help="""Use deviceName as serial input device.
                    default is {}""".format(DEFAULTDEVICE))

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
    #args = parseMyArgs()
    run()
