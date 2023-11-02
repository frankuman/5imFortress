"""
Modbus master
This file communicates with server/slave via modbustcp and dashboard
"""
import datetime
#from time import sleep
#from random import uniform
import logging
from pyModbusTCP.client import ModbusClient
from frontend.datalogger import logger

client = ModbusClient(host = "127.0.0.1", port = 502, auto_open = True, auto_close = True, timeout = 1) #, debug=True

def start_client():
    """
    Setup for modbus client/master
    Start client/master and set up logging
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
    logger.log(0, log)

    print("Master is online...")
    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_MASTER] Master is online..."
    logger.log(0, log)

    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_MASTER] Slave connection -  1:{slave_up_list[0]}, 2:{slave_up_list[1]}, 3:{slave_up_list[2]}, 4:{slave_up_list[3]}, 5:{slave_up_list[4]}"
    logger.log(0, log)

def get_bitrate(bs_id):
    """
    Calls the read_register to get the bitrate registers
    """
    #Calculate address for bitrate register
    bitlist = read_register(bs_id = bs_id, choice = "BITR")
    #convert to readable
    return bitlist

def get_users(bs_id):
    """
    Calls the read_register to get user registers
    """
    users = read_register(bs_id, "USR")
    return users

def change_gain(gain_list):
    """
    Write to holding register the value of antenna gain
    """
    write_register(0, gain_list, "GAIN")
    return True

def read_register(bs_id, choice):
    """
    Reads registers on address calculated by id and choice
    data is "function code" and determines address and length to read
    """
    #read bitrate registers
    if choice == "BITR":
        bitrate = []
        bitrate_1 = []
        print("\n",client.last_error_as_txt)
        addr = (bs_id - 1) * 8
        for _ in range(4):
            bitrate_1.append(client.read_input_registers(addr, 1)[0])
            addr += 1

        bitrate_2 = []
        addr = (bs_id - 1) * 8 + 4
        for _ in range(4):
            bitrate_2.append(client.read_input_registers(addr, 1)[0])
            addr += 1

        bitrate.append(sum(bitrate_1))
        bitrate.append(sum(bitrate_2))
        return bitrate

    if choice == "USR":
        users = 0
        addr = 100 + (bs_id - 1) * 2
        for _ in range(2):
            users += client.read_input_registers(addr, 1)[0]
            addr += 1

        return users
    return False

def write_register(bs_id, data, choice):
    """
    Write to holding register, address calculated with bs_idand choice.
    Data gets written to holding register.
    """
    if choice == "GAIN":
        gain_addr = 50
        ret = client.write_multiple_registers(gain_addr, data)
        print("gain return: ", ret)
        return True
    return False

def read_coil():
    """
    Reads coils
    """
    #read 5 bits contining statuses for bs's
    coil_bitrate = client.read_coils(0, 5)
    print("coil", coil_bitrate)

def write_coil(bs_id = None, value = None, data = None, addr = None):
    """
    Writes value into address pointed to by id or addr
    """
    #print("[Debug] trying to write", id, " to give it,", value)

    if data == "POW":
        addr = bs_id

    a = client.write_single_coil(addr, value)
    #print("[Debug] Wrote to coil", id, " and gave it value,", value)
    if a is True:
        pass
    else:
        print("ERROR: Can't write to coil - ",addr)
        current_time = datetime.datetime.now()

        time_string = current_time.strftime('%H:%M:%S')
        log = f"({time_string})-[MODBUS_MASTER] ERROR: Can't write to coil - " + addr
        logger.log(0, log)
