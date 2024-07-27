"""
Update History:
* Tue Apr 29 2024 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation
* Tue Jul 23 2024 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - Add epicserverhttp.py
-          Add a simple HTTP server that will fetch 
-          and display powergate status as a very
-          simple web page. First pass, functional
-          but needs work to make it easier to read.
* Fri Jul 26 2024 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.3 - Add epicData class to parse and hold the
-          powergate status, then display it in a
-          more readable format.  The epicsererhttp
-          module was also updated to use the new
-          class. We're getting close to a release.

"""
VERSION = '0.0.2'
PORT = 7373
DEFAULTDEVICE = '/dev/ttyACM0'
CALLSIGN = 'N0SO'

