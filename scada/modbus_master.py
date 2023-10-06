from pyModbusTCP.client import ModbusClient
from time import sleep
from random import uniform

client = ModbusClient(host="127.0.0.1")

def start_client():
    a = client.write_single_coil(1,1)
    print(a)
    client.open()
    
    #Nothing happens after this!
    

def read_coil():
    coil_bitrate = client.read_coils(0,5)
    print("coil",coil_bitrate)

def write_coil(addr, value):
    a = client.write_single_coil(addr,value)
    print(a)

# write_status_coil(id)
#       coil(1) = true-false

# write_status_bs_1()
        #coil(1) = true-false

