from time import sleep
from random import uniform
import logging
from pyModbusTCP.client import ModbusClient
from datalogger import logger
import datetime
client = ModbusClient(host = "127.0.0.1", port = 502, auto_open = True, auto_close = True, timeout = 1)

def start_client():
    """
    Setup for modbus client/master
    """
    logging.basicConfig()
    a = client.open()
    print("CLIENT: ", a)
    slave_up_list = []
    for i in range(1, 6):
        a = client.write_single_coil(i, 1)
        slave_up_list.append(a)

    current_time = datetime.datetime.now()
    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_MASTER] Master starting on 127.0.0.1:502"
    logger.log(0,log)

    print("Master is online...")
    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_MASTER] Master is online..."
    logger.log(0,log)

    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_MASTER] Slave connection -  1:{slave_up_list[0]}, 2:{slave_up_list[1]}, 3:{slave_up_list[2]}, 4:{slave_up_list[3]}, 5:{slave_up_list[4]}"
    logger.log(0,log)

def get_bitrate(id):
    """
    Calls the right input register
    """
    #Calculate address for bitrate register
    #0x3000 and 128 bits for each tower
    #addr = 12288 + id*128
    bitlist = read_register(id = id, data = "BITR")
    #convert to readable
    return bitlist

def read_register(id, data):
    if data == "BITR":
        bitrate = []
        # addr = 12288 + id * 128
        # bitrate.append(sum(client.read_input_registers(addr, 4)))
        # addr = 12288 + id * 128 + 64
        # bitrate.append(sum(client.read_input_registers(addr, 4)))

        bitrate_1 = []
        #addr = 12288 + id * 128
        addr = id * 8
        for i in range(4):
            bitrate_1.append(client.read_input_registers(addr, 1)[0])
            addr += 1

        bitrate_2 = []
        #addr = 12288 + id * 128 + 16
        addr = id * 8 + 4
        for i in range(4):
            
            bitrate_2.append(client.read_input_registers(addr, 1)[0])
            addr += 1

        print(bitrate_1)
        print(bitrate_2)
        bitrate.append(sum(bitrate_1))
        bitrate.append(sum(bitrate_2))

        
        return bitrate

def read_coil():
    coil_bitrate = client.read_coils(0, 5)
    print("coil", coil_bitrate)

def write_coil(id = None, value = None, data = None, addr = None):
    """
    Writes value into address pointed to by id or addr
    """
    #print("[Debug] trying to write", id, " to give it,", value)

    if data == "POW":
        addr = id

    a = client.write_single_coil(addr, value)
    #print("[Debug] Wrote to coil", id, " and gave it value,", value)
    if a is True:
        pass
    else:
        print("ERROR: Can't write to coil - ",addr)
        current_time = datetime.datetime.now()

        time_string = current_time.strftime('%H:%M:%S')
        log = f"({time_string})-[MODBUS_MASTER] ERROR: Can't write to coil - "+addr
        logger.log(0,log)

