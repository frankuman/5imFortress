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

POWER_ADDR_COIL = 1
BITRATE_ACTIVE_ADDR_REG = 1
BITRATE_TOTAL_ADDR_REG = 5
USERS_ADDR_REG = 9
GAIN_ADDR_REG = 11

client1 = ModbusClient(host = "127.0.0.1", port = 502, auto_open = True, auto_close = True, timeout = 1)
client2 = ModbusClient(host = "127.0.0.1", port = 503, auto_open = True, auto_close = True, timeout = 1)
client3 = ModbusClient(host = "127.0.0.1", port = 504, auto_open = True, auto_close = True, timeout = 1)
client4 = ModbusClient(host = "127.0.0.1", port = 505, auto_open = True, auto_close = True, timeout = 1)
client5 = ModbusClient(host = "127.0.0.1", port = 506, auto_open = True, auto_close = True, timeout = 1)
clients = [client1, client2, client3, client4, client5]


def start_client():
    """
    Setup for modbus client/master
    Start client/master and set up logging
    """
    logging.basicConfig()
    slave_up_list = []
    for client in clients:
        a = client.open()

        print("CLIENT: ", a)

        a = client.write_single_coil(POWER_ADDR_COIL, 1)
        slave_up_list.append(a)
        f = client.write_multiple_coils(2, [1,1,1,1])

    current_time = datetime.datetime.now()
    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_MASTER] Master starting"
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

def change_gain(bs_id, gain):
    """
    Write to holding register the value of antenna gain
    """
    write_register(bs_id, gain, "GAIN")
    return True

def change_antenna_power(bs_id, antenna_id, status):
    write_coil(bs_id, status, "ANTENNA", antenna_id+1)
    return True

def read_register(bs_id, choice):
    """
    Reads registers on address calculated by id and choice
    data is "function code" and determines address and length to read
    """
    #read bitrate registers
    
    client = clients[bs_id - 1]
    if choice == "BITR":
        bitrate_list = []
        bitrate = client.read_input_registers(BITRATE_ACTIVE_ADDR_REG, 8)
        if bitrate is None:
            return False
        bitrate_list.append(sum(bitrate[0:4]))
        bitrate_list.append(sum(bitrate[4:]))

        return bitrate_list

    if choice == "USR":
        users = sum(client.read_input_registers(USERS_ADDR_REG, 2))
        return users
    print("One bitrate error here with", bs_id)
    return False

def write_register(bs_id, data, choice):
    """
    Write to holding register, address calculated with bs_idand choice.
    Data gets written to holding register.
    """
    client = clients[bs_id - 1]
    if choice == "GAIN":
        client.write_single_register(GAIN_ADDR_REG, data)
        return True
    return False

def read_coil(bs_id):
    """
    Reads coils
    """

    client = clients[bs_id - 1]
    #read 5 bits contining statuses for bs's
    coil_bitrate = client.read_coils(0, 5)
    print("coil", coil_bitrate)

def write_coil(bs_id = None, value = None, data = None, addr = None):
    """
    Writes value into address pointed to by id or addr
    """
    #print("[Debug] trying to write", id, " to give it,", value)

    if data == "POW":
        addr = POWER_ADDR_COIL
    client = clients[bs_id - 1]

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
