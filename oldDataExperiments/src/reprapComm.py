# This file is part of the 3DEMscanner measurement suite.
# 
# 3DEMscanner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# 3DEMscanner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with 3DEMscanner.  If not, see <http://www.gnu.org/licenses/>.
#
# Purpose of the file: process reprap movement and generate measurement path

from serial import Serial
import glob
import os

class RepRap(object):
    def __init__(self, baudRate):
        self.debug = False
        self.port = self.testPortsForRepRap()
        self.baud = baudRate
        
        print("Found RepRap on port: ")
        print(self.port)
        
        if ("ACM" in self.port):
            self.printer = Serial(self.port, self.baud, timeout = 5)
            print(self.printer.readline().strip().decode('ascii')) #without these readout nothing moves ??? strange but true
            print(self.printer.readline().strip().decode('ascii'))
            print(self.printer.readline().strip().decode('ascii'))
            print(self.printer.readline().strip().decode('ascii'))
            print(self.printer.readline().strip().decode('ascii'))
            print(self.printer.readline().strip().decode('ascii'))
            print(self.printer.readline().strip().decode('ascii'))
            print(self.printer.readline().strip().decode('ascii'))
            print("send: G91")
            word = 'G91\r\n'
            self.printer.write(word.encode('ascii'))
            print(self.printer.readline().strip().decode('ascii'))

    def scanForSerialPorts(self):
        """scan for available ports. 
        return a list of device names. 
        """
        baselist=[]
        if os.name == "nt" :
            try:
                import winreg #@UnresolvedImport
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"HARDWARE\\DEVICEMAP\\SERIALCOMM")
                i = 0
                while(1):
                    baselist += [winreg.EnumValue(key,i)[1]]
                    i += 1
            except:
                pass
        if os.name == "posix" :
            pass
    
        return baselist+glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') + glob.glob("/dev/tty.*") + glob.glob("/dev/cu.*") + glob.glob("/dev/rfcomm*")

    def testPortsForRepRap(self):
        """ Test found available port from scanserial() function 
        returns 'port name' or 'none' """
    
        self.portOk = "none" # port that will be used for communication with RepRap
    
        portName = self.scanForSerialPorts()
        if self.debug:
            print(portName)
            print("Number of ports found: ", len(portName))
        else:
            pass
        
        num = len(portName)
    
        try:    
            for portName[num-1] in portName:
                printer = Serial(portName[num-1], 115200, timeout = 30)
            
                answer = printer.readline().strip()
                printer.close()
                #print(answer.decode('ascii'))
                if ("Sprinter" in answer.decode('ascii')):
                    self.portOk = portName[num-1]
                    if self.debug:
                        print("OK port is: ", self.portOk)
                    else:
                        pass
                else:
                    pass
        except:
            print("Something happend, don't know yet.")
           
        if self.portOk is not "none":            
            return self.portOk
        else:
            return self.portOk
            print("Port not found.")
        
    def disconnect(self):
        try:
            self.printer.close()
            print("RepRap printer is now disconnected.")
        except:
            print("RepRap is not connected")
        
    def checkForValidAxis(self, axis):
        """ Checks input parameters for the movement
        Returns True or False. """
        allowed = ["X","Y","Z","E"]
        if self.debug:
            print(allowed)
            print("Axis is: ")
            print(axis)
        else:
            pass    
        if axis in allowed:
            return True
        else:
            return False
        
    def checkForValidDirection(self, direction):
        """ Checks input parameters for the direction
        Returns True or False. """
        allowed = ["+","-"]
        if self.debug:
            print(allowed)
            print("Direction is: ")
            print(direction)
        else:
            pass
        if direction in allowed:
            return True
        else:
            return False 
    
    def move(self, axis, direction, value, speed):
        """ Moves given 'axis' in '+' or '-' 'direction' with 'value' and 'speed'
       
        """
        word = "none"
        moveAxis = "none"
        moveDirection = "none"
    
        if self.checkForValidAxis(axis):
            moveAxis = axis
        else:
            print("Axis definition Error. Please enter \"X\", \"Y\", \"Z\", \"E\".")
        
        if self.checkForValidDirection(direction):
            moveDirection = direction
        else:
            print("Direction definition Error. Please enter \"+\", \"-\".")
        
        #axis = str(axis)   # X, Y, Z, E
        direction = str(direction)  # '+' or '-'
        value = str(value)  # relative move 
        speed = str(speed)  # set speed of movement from 0 to 3000

        if moveAxis is not "none":
            word = "G1 " + moveAxis
        else:
            word = "none"
    
        if moveDirection is not "none":
            word = word + moveDirection
        else:
            word = "none"
    
        if word is not "none":
            word = word + value + " F" + speed + "\r\n"
            if self.debug:
                print(word)
            else: 
                pass
        
            return word.encode(encoding='ascii', errors='strict')
        else:
            pass
