#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from __init__ import VERSION, DEFAULTDEVICE, PORT, CALLSIGN
from epicmon import epicMon, epicData
from datetime import datetime

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
                gateStat.cpuTemp = pgate.getcpuTemp()[0]
                self.ShowHTML(gateStat)
                #gateStat.showValues()
        elif self.path == '/exit':
            print('Server exiting... bye!')
            exit()

    def ShowHTML(self, dataList):
        now = datetime.now()
        strtime = now.strftime("%Y-%m-%d %H:%M:%S")
        htdoc = """<!DOCTYPE html>
                    <html>
                    <head>
                    <title>{}  Mobile Power Status</title>
                    <meta http-equiv="refresh" content="60">
                    </head>
                    <body>
                    <h1 align='center'>{}  Mobile Power Status</h1>
                    <p align='center'>Updated: {}</p>
                    <hr>""".format(CALLSIGN, CALLSIGN, strtime)
        #for l in dataList:
        htdoc += '<p>{}<br>{}</p>'.format(dataList.deviceStg, 
                                          dataList.configStg)
        htdoc += """<p>Vehicle Battery Voltage: {} V<br>
                       Charge State: {}<br>
                       Time in current state: {} minutes<br>
                       Rack Battery Voltage: {} V<br>
                       Current: {} A<br>
                       Solar Volts: {} V<br>
                       Rack Battery Temperature: {} F<br>
                       Host CPU Temperature: {} C<br>
                 </p>""".format(dataList.psVolts,
                                dataList.battState,
                                dataList.inStateTime,
                                dataList.battVolts,
                                dataList.battAmps,
                                dataList.solarVolts,
                                dataList.pgateTemp,
                                dataList.cpuTemp)
        """
        htdoc += "<p>Raw Data:<br>{}<br>\n".format(dataList.rawStatus[8])
        htdoc += "{}<br></p>\n".format(dataList.rawStatus[9])
        """
        htdoc += """</body>
                </html>"""
        self.wfile.write(htdoc.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print("Starting server on port {}...".format(PORT))
    httpd.serve_forever()
