from telnetlib import Telnet
from time import sleep

termChar = "\n"            # termination character should be \n
host = "10.1.15.106"    # IP address of PNA
port = "5024"           # connection port
debugCommunication = False  # add all prints

def initConnection(host, port, timeout):
    """initiate connection to PNA and returns Telnet object tn
    
    if connection is succesfull returns object tn
    """
    try:
        tn = Telnet(host, port, timeout)
        ans = tn.read_until("SCPI> ".encode(encoding='ascii', errors='strict'), timeout = 10).decode('ascii').strip()
        
        if debugCommunication:
            print(ans)
        else:
            pass
        
        tn.write("*IDN?".encode(encoding='ascii', errors='strict'))
        tn.write(termChar.encode(encoding='ascii', errors='strict'))   # just send ENTER to execute the command
        
        ans = tn.read_until("SCPI> ".encode(encoding='ascii', errors='strict'), timeout = 5).decode('ascii').strip()
        
        if debugCommunication:
            print(ans)
        else:
            pass   
        
        return tn
    
    except:
        print("Error while connecting.")
        
def closeConnection(telnetConnection):
    """Closes the connection to the PNA
    
    Closes the connection to PNA.
    If the connection is already closed print message.
    """
    try:
        telnetConnection.close()
        if debugCommunication:
            print("Connection to PNA closed.")
        else:
            pass
    except:
        if debugCommunication:
            print("Connetion to PNA already closed.")
        else:
            pass
        
def sendCommand(message):
    """sends SCPI command to PNA
    
    Can block if the connection is blocked.
    May raise socket.error if the connection is closed.
    """
    try:
        msg = message + termChar
        tn.write(msg.encode(encoding='ascii', errors='strict'))
        if debugCommunication:
            print("Message send to PNA: ")
            print(msg.encode(encoding='ascii', errors='strict'))
        else:
            pass        
    except:
        print("No connection with the PNA - socket.error.")
    
def readMessage(telnetConnection):
    """ prints in console the message from PNA until 'SCPI>'
    
    Reads the data message from PNA.
    If no connection returns message.
    """
    try:
        answer = tn.read_until("SCPI> ".encode(encoding='ascii', errors='strict'), timeout = 10).decode('ascii').strip()
        return answer
        if debugCommunication:
            print(answer)    
        else:
            pass 
    except:
        print("Nothing from PNA.")

def askPNA(telnetConnection, message):
    """ send message to PNA and prints the answer
    
    sends "message" given as an input and 
    returns the answer from PNA as a result
    """
    try:
        sendCommand(message)
        # send_command("*WAI")
        answer = readMessage(telnetConnection)
        return answer
    except:
        print("Please enter: object to PNA, valid string data")
    
tn = initConnection(host, port, 10)
print(tn)

print("Reset PNA display: syst:fpr")
sendCommand("syst:fpr")

print("Current working folder: ")
print(askPNA(tn, "mmem:cdir?"))

print("Load default displays and calibration.")
sendCommand("mmem:load 'calibrationRado.csa'")

print("Names and parameters of existing measurements for the specified channel:")
print(askPNA(tn, "calc:par:cat?"))

print("System error ?: ")
print(askPNA(tn, "SYSTEM:ERROR?"))

sendCommand("format:data ascii")
sendCommand("calc:par:mnum 1")
print("format of the stored snp: ")
print(sendCommand("mmem:stor:trace:format:snp?"))
print(sendCommand("mmem:stor:trace:format:snp db"))
print(askPNA(tn, "calc:data? fdata"))

#sleep(15)

print("System error ?: ")
print(askPNA(tn, "SYSTEM:ERROR?"))

closeConnection(tn)
print("quit")

#print("Select channel and measured parameter:")
#print(askPNA(tn, "CALCulate:PARameter:SELect 'S21-Phase'"))
#
#print("ask1: ")
#print(askPNA(tn, "SENSe1:SWEep:POIN?"))
#
#print("ask2: set sweep points to 10")
#print(askPNA(tn, "SENSe1:SWEep:POIN 10"))
#
#print("ask3: ")
#print(askPNA(tn, "SENSe1:SWEep:POIN?"))
#
#print("ask5: ")
#print(askPNA(tn, "CALCulate1:DATA? FDATA"))
#
##print("ask5: ")
##print(askPNA(tn, "CALCulate:DATA? FDATA"))

#send_command("SYSTem:PRESet;*wai")
#read_message(tn)
#send_command("SENSe1:SWEep:POIN?")
#read_message(tn)
#send_command("INITiate:CONTinuous OFF")
#read_message(tn)
#send_command("INITiate:IMMediate;*wai")
#read_message(tn)
#send_command("DISP:WIND2:STATE off")
#read_message(tn)
#send_command("DISP:ARR QUAD")
#read_message(tn)
#
#send_command("CALCulate2:PARameter:DEFine:EXT 'Meas2',S21")
#read_message(tn)
#send_command("DISPlay:WINDow4:TRACe1:FEED 'Meas2'")
#read_message(tn)
#
#send_command("*OPC?")
#read_message(tn)
#
#send_command("*TST?")
#read_message(tn)
#send_command("*CLS")
#read_message(tn)
# PEP8 convetntion
# Use single quotes for enums, and double quotes for strings
#
# Sample working communication
#SCPI> *IDN?
#Agilent Technologies,N5230C,MY49001380,A.09.42.01
#SCPI> DISPlay:WINDow1:STATE ON                    # turns window 1 on
#SCPI> DISPlay:WINDow2:STATE ON                    # turns window 2 on
#SCPI> DISP:WIND3:STATE ON                         # turns window 3 on
#SCPI> DISP:WIND4:STATE ON                         # turns window 4 on
#SCPI> DISP:WIND2:STATE OFF                        # turns window 2 off
#SCPI> DISP:WIND3:STATE OFF                        # turns window 3 off
#SCPI> DISP:WIND4:STATE OFF                        # turns window 4 off
#SCPI> DISPlay:CATalog?                            # number of displays shown
#"1"
#SCPI> SENSe1:FREQuency:START 1ghz               # set start frequency
#SCPI> SENSe1:FREQuency:STOP 2ghz                # set stop frequency
#SCPI> CALC:PAR:CAT:EXT?                         # Returns the names and parameters of existing measurements for the specified channel.
#                                                # This command lists receiver parameters with "_" such that R1,1 is reported as R1_1. 
#                                                # This makes the returned string a true "comma-delimited" list all the time.
#                                                # Return type - String - "<measurement name>,<parameter>,[<measurement name>,<parameter>...]"
#                                                # Default - "CH1_S11_1,S11"
#"CH1_S11_1,S11,CH1_S22_2,S22,CH1_S21_3,S21"
#
# DISP:ARR CASC
# display:arrange cascade
# Window arrangement. Choose from:
# TILE - tiles existing windows
# CASCade - overlaps existing windows
# OVERlay - all traces placed in 1 window
# STACk - 2 windows
# SPLit - 3 windows
# QUAD - 4 windows
