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
* Sat Jul 27 2024 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.4 - Updated the status parsing method to use
-          fixed character positions for the status
-          parts (voltage, current, etc.) Works much
-          better and the powergate appears to put 
-          them in the same columns each time. More
-          testing needed.
* Sun Jul 28 2024 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.5 - Added inStateTime to epicData to store the
-          parameter "Time in current charge state".
* Sun Sep 08 2024 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.6 - Added script activate to setup a 'virtual
-          environment' to execute in. This should 
-          make it easier to build a distribution 
-          package in the future. It does require 
-          running 'source bin/activate' to setup the
-          virtual environment. It eliminates the code
-          previously required to add the epicmon module
-          to the python path. That code would need to
-          be removed for a release. This technique was
-          'borrowed' from the Meshtastic CLI project.
-
"""
VERSION = '0.0.6'
PORT = 7373
DEFAULTDEVICE = '/dev/ttyACM0'
CALLSIGN = 'N0SO'

