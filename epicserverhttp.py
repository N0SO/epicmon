#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from __init__ import VERSION, DEFAULTDEVICE, PORT, CALLSIGN, SLEEPTIME
from epicmon import epicMon, epicData
from datetime import datetime
from time import sleep
import subprocess

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if (self.path == '/restart'):
            #restart the http server
            st = 3
            str = f'Restarting epicserver in {st} seconds...'
            htdoc=f"""<html>
                      <body>
                      <h1 align='center'>{str}</h1>
                      </body>
                      </html>"""
            print(str)
            self.wfile.write(htdoc.encode('utf-8'))
            sleep(st)
            result=subprocess.call(['sudo systemctl restart epicserve'], shell=True)

        elif (self.path == '/reboot'):
            #Reboot host system
            str = f'Rebooting system in {SLEEPTIME} seconds...'
            print (str)
            htdoc = f"<html><body><p align='center'>{str}</p></body></html>"
            self.wfile.write(htdoc.encode('utf-8')) 
            sleep(SLEEPTIME)
            result = subprocess.call(['sudo', 'reboot'])
            subprocess.call(['sudo reboot'], shell=True)
            result = subprocess.call('sudo reboot', shell=True)
            print (f'sudo reboot result ={result.returncode}')

        elif (self.path == '/shutdown'):
            #Shutdown host system for power off
            print (f'Shutting down system in {SLEEPTIME} seconds...')
            sleep(SLEEPTIME)
            result=subprocess.call(['sudo poweroff'], shell=True)
            print (f'sudo poweroff result ={result.returncode}')

        elif self.path == '/exit':
            #Exit http server - result in systemctl restarting it
            #if started using the systemctl service.
            print('Server exiting... bye!')
            self.wfile.write("""<html>
                                <body>
                                <h1>Server Exiting (html)... bye!</h1>
                                </body>
                                </html>""".encode('utf-8'))
            #sleep(10)
            exit()

        elif (self.path == '/') or (self.path == '/getstatus'):
            #Show epic powergate status
            #if args.deviceName:
            pgate = epicMon(DEFAULTDEVICE)
            if pgate:
                gateStat = epicData(pgate.get_status())
                gateStat.cpuTemp = pgate.getcpuTemp()[0]
                self.ShowHTML(gateStat)
                #gateStat.showValues()
        else:
            str = f'Invalid path: {self.path}'
            print (str)
            htdoc = f"<html><body><p align='center'>{str}</p></body></html>"
            self.wfile.write(htdoc.encode('utf-8')) 
            


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
        htdoc += '<p>{}</p><p>{}</p>'.format(dataList.deviceStg, 
                                          dataList.configStg)
        htdoc += """<p><b>Vehicle Battery Voltage:</b> {} V</br>
                      <b>Charge State:</b> {}</br>
                      <b> Time in current state:</b> {} minutes</br>
                      <b> Rack Battery Voltage:</b> {} V</br>
                      <b> Current:</b> {} A</br>
                      <b> Solar Volts:</b> {} V</br>
                      <b> Rack Battery Temperature:</b> {} F</br>
                      <b> Host CPU Temperature:</b> {} C</p>
                       """.format(dataList.psVolts,
                                dataList.battState,
                                dataList.inStateTime,
                                dataList.battVolts,
                                dataList.battAmps,
                                dataList.solarVolts,
                                dataList.pgateTemp,
                                dataList.cpuTemp)

        htdoc += f"""<hr>
                    <p> <a href='http://pimobile:{PORT}/restart' target="_blank" rel="noopener noreferrer">RESTART Epic Server</a></p>
                    <p> <a href='http://pimobile:{PORT}/reboot' target="_blank" rel="noopener noreferrer">REBOOT Epic Server CPU</a></p>
                    <p> <a href='http://pimobile:{PORT}/shutdown' target="_blank" rel="noopener noreferrer">SHUTDOWN  Epic Server CPU</a></p>
                    <p> <a href='http://pimobile:{PORT}/exit' target="_blank" rel="noopener noreferrer">exit server</a></p>
                 """

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
