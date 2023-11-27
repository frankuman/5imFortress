import socket
from time import sleep
import sys

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
spacer = ' ' * 1  # Space between funny menu text and guy.
for a, b in zip(MENUTEXT.splitlines(), MENUSKULL.splitlines()):
    print(f'{a}{spacer}{b}')
print("\nwww.github.com/frankuman/5imFortress   \n")

def menu():
    #Arguments
    parser = argparse.ArgumentParser(description="\n\nHelp")
    parser.add_argument("-write-coil", action="store_true", help="Write to coil")
    parser.add_argument("-write-register", action="store_true", help="Write to single register")
    parser.add_argument("-loop", action="store_true", help="Loop a functrion n times")
    parser.add_argument("-n", type=int, help="How many loops")
    parser.add_argument("-t", type=float, help="Loop timeout in seconds")

    parser.add_argument("-addr", type=int, help="Register/coil address")
    parser.add_argument("-val", type=int, help="Value to write (0 or 1)")
    parser.add_argument("-ip", type=str, help="Target IP address")
    parser.add_argument("-port", type=int, help="Target port")
    parser.add_argument("-id", type=int, default=1, help="Modbus slave ID (default: 1)")
    args = parser.parse_args()

    if args.loop:
        if args.n is None or args.addr is None or args.val is None or args.ip is None or args.port is None:
            print("Error: --n, --add")
            return
        if args.write_coil:
            setup_loop(write_coil,args.n,args.t,args.addr, args.val, args.ip, args.port, args.id)
        elif args.write_register:
            setup_loop(write_register,args.n,args.t,args.addr, args.val, args.ip, args.port, args.id)
        else:
            print("Error: Please specify a valid operation (-write-coil|-write-register)")
            return
    elif args.write_coil:
        if args.addr is None or args.val is None or args.ip is None or args.port is None:
            print("Error: -register, -value, -address, and -port are required for -write-coil")
            return
        write_coil(args.addr, args.val, args.ip, args.port, args.id)
    elif args.write_register:
        write_register(args.addr, args.val, args.ip, args.port, args.id)
    else:
        print("Error: Please specify a valid operation (-write-coil)")

def setup_loop(function, n,t,register,value,address,port,slave_id = 1):
    for i in range(n):
        function(register,value,address,port,slave_id)
        print("["+str(i)+"/"+str(n)+"]")
        sleep(t)

def write_register(register,value,address,port,slave_id = 1):
    transaction_identifier = b"\x18\x03"
    protocol_identifier = b"\x00\x00"
    lenght_field = b"\x00\x06"
    mod_function = b"\x06"
    exception_code = b'\x86'


    slave_address = bytes([int(slave_id)])
    register = (int(register)).to_bytes(2,'big')
    byte_value = (int(value)).to_bytes(2,'big')
    data = register + byte_value

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.settimeout(3)

        s.connect((address,int(port)))
        payload = transaction_identifier + protocol_identifier + lenght_field + slave_address + mod_function + data
        s.send(payload)
        response = s.recv(256)
        s.close()

        if (response[0:5] == b"\x18\x03\x00\x00\x00") and (response[7:8] == mod_function) :
            print("\n[+]WRITTEN VALUE: "+str(int.from_bytes(response[-2::],'big')))
        elif 	(response[0:5] == b"\x18\x03\x00\x00\x00") and (response[7:8] == exception_code) :
            print("[-] Exception thrown:")
            print(Exception(response[8:9]))
        else:
            print("[-] Operation failed...Error getting ModBus response...")
    except:
        print("[-] Host seems offline... ")

def write_coil(register,value,address,port,slave_id = 1):
    transaction_identifier = b"\x18\x03"
    protocol_identifier = b"\x00\x00"
    length_field = b"\x00\x06"
    mod_function = b"\x05"
    byte_on = b"\xff\x00"
    byte_off = b"\x00\x00"
    exception_code = b'\x85'

    
    slave_address = bytes([int(slave_id)])
    register = (int(register)).to_bytes(2,'big')
    
    try:
        #Depending if we wanna turn it on or off it might be + 0 or +255
        if value == 0 :
            complete_data = register + byte_off
        else:
            complete_data = register + byte_on

        # Create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set socket options to reuse the address and set a timeout of 3 seconds
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(3)

        # Connect to the specified address and port
        s.connect((address, int(port)))

        # Construct the payload for the ModBus operation
        payload = transaction_identifier + protocol_identifier + length_field + slave_address + mod_function + complete_data

        # Send the payload to the server
        s.send(payload)

        # Receive the response (up to 256 bytes)
        response = s.recv(256)

        # Close the socket
        s.close()

        # Check the ModBus response for success or failure
        if (response[0:5] == b"\x18\x03\x00\x00\x00") and (response[7:8] == mod_function):
            # Print the written value if the response indicates success
            print("\n[+] WRITTEN VALUE: " + str(int.from_bytes(response[-2:-1], 'big')))
        elif (response[0:5] == b"\x18\x03\x00\x00\x00") and (response[7:8] == exception_code):
            # Print an exception if the response indicates an exception
            print("[-] Exception thrown:")
            print(Exception(response[8:9]))
        else:
            print("[-] Operation failed... Error getting ModBus response...")
    except Exception as e:
        print("[-] Error:", e)

if __name__ == "__main__":
    menu()

    #!/usr/bin/python3
