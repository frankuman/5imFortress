from pyModbusTCP.client import ModbusClient
from time import sleep
from random import uniform

def read_coils():
    client = ModbusClient(host="127.0.0.1")
    while True:
        sleep(2)
        
