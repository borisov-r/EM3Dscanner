from telnetlib import Telnet
"""
class PNA(host, port, timeout):
    def initConnection(host, port, timeout):
    #
    #initiate connection to PNA and returns Telnet object tn
    #if connection is succesfull returns object tn
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
    def __init__(self):
        tn = initConnection(host, port, timeout)
        
class Messages:
    message1 = ""        
"""
tn = Telnet('10.1.15.106','5024',timeout=5)
ans = tn.read_until("SCPI> ".encode(encoding='ascii', errors='strict'), timeout = 10).decode('ascii').strip()
print(ans)

message1 = 'calc:data:snp:ports? \"1,2\"\n'
message2 = "*IDN?"
message3 = "system:error?"

tn.write(message1.encode(encoding='ascii', errors='strict'))
ans = tn.read_until("SCPI> ".encode(encoding='ascii', errors='strict'), timeout = 10).decode('ascii').strip()
print(ans)

# Filename
filename = "point001"
# Create a file object:
# in "write" mode
FILE = open(filename,"w")
#print(simple)

# Write all the lines at once:
FILE.writelines(ans)
FILE.close()