
import socket
from time import sleep
import sys

transaction_identifier = b"\x18\x03"	
protocol_identifier = b"\x00\x00"	
lenght_field = b"\x00\x06"		
mod_function = b"\x05"
byte_on = b"\xff\x00"
byte_off = b"\x00\x00"
exception_code = b'\x85'

MENUTEXT = r"""
 .d8888b.               d8888 
d88P  Y88b             d88888 
888    888            d88P888 
888                  d88P 888 
888  88888          d88P  888 
888    888 888888  d88P   888 
Y88b  d88P        d8888888888 
 "Y8888P88       d88P     888 
                              
"""
MENUSKULL = r"""
   ,    ,    /\   /\
  /( /\ )\  _\ \_/ /_
  |\_||_/| < \_   _/ >
  \______/  \|0   0|/
    _\/_   _(_  ^  _)_
   ( () ) /`\|V''''V|/`\
     {}   \  \_____/  /
     ()   /\   )=(   /\
     {}  /  \_/\=/\_/  \
"""
import argparse
TARGETS = []
spacer = ' ' * 1  # Space between cards.
for a, b in zip(MENUTEXT.splitlines(), MENUSKULL.splitlines()):
    print(f'{a}{spacer}{b}')
print("\nwww.github.com/frankuman/5imFortress   \n")
def menu():
    parser = argparse.ArgumentParser(description="\n\nHelp")
    parser.add_argument("-write-coil", action="store_true", help="Write to coil")
    parser.add_argument("-reg", type=int, help="Register address")
    parser.add_argument("-val", type=int, help="Value to write (0 or 1)")
    parser.add_argument("-addr", type=str, help="Target IP address")
    parser.add_argument("-port", type=int, help="Target port")
    parser.add_argument("-id", type=int, default=1, help="Modbus slave ID (default: 1)")
    args = parser.parse_args()

    if args.write_coil:
        if args.reg is None or args.val is None or args.addr is None or args.port is None:
            print("Error: --register, --value, --address, and --port are required for --write-coil")
            return
        write_coil(args.reg, args.val, args.addr, args.port, args.id)
    else:
        print("Error: Please specify a valid operation (--write-coil)")



def write_coil(register,value,address,port,slave_id = 1):
    slave_address = bytes([int(slave_id)])
    register = (int(register)).to_bytes(2,'big')
    try:
        if value == 0 :
            complete_data = register + byte_off
        else:
            complete_data = register + byte_on
            
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.settimeout(3)

        s.connect((address,int(port)))
        payload = transaction_identifier + protocol_identifier +lenght_field + slave_address + mod_function + complete_data
        s.send(payload)
        response = s.recv(256)
        s.close()

        if (response[0:5] == b"\x18\x03\x00\x00\x00") and (response[7:8] == mod_function) :
            print("\n[+]WRITTEN VALUE: "+str(int.from_bytes(response[-2:-1],'big')))
        elif 	(response[0:5] == b"\x18\x03\x00\x00\x00") and (response[7:8] == exception_code) :
            print("[-] Exception thrown:")
            print(exception(response[8:9]))
        else:
            print("[-] Operation failed... Error getting ModBus response...")
    except:
        print("[-] Host is offline or you specified a wrong port...")
		
        


if __name__ == "__main__":
    menu()

    #!/usr/bin/python3

