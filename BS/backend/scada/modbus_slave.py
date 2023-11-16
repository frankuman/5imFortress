"""
This file connects modbus communicates with modbus client/master via modbustcp protocol
"""
import datetime
#from pyModbusTCP.server import DataBank, ModbusServer
from BS.backend.helpers import slave_data_handler as class_handler
from BS.backend.datalogger import logger

POWER_ADDR_COIL = 1
BITRATE_ACTIVE_ADDR_REG = 1
BITRATE_TOTAL_ADDR_REG = 5
USERS_ADDR_REG = 9
GAIN_ADDR_REG = 11

#Initiate data_bank for server, with all coils as 1
#to make sure all towers start with status UP
print('Creating new instance')


server_man = class_handler.server_manager().instance()

def start_server():
    """"
    Start modbus server and loop for updating status coils
    """
    # try:
    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_SLAVE] Slave starting on 127.0.0.1:502"
    logger.log(0,log)
    print(log)
    #log = "Starting slave..."

    #server.start()
    for i in range(1,6):
        start_slave(i)

    print("[MODBUS_SLAVE] Server is online")
    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_SLAVE] Server is online"
    logger.log(0,log)
    print(log)

def start_slave(bs_id):
    """
    Start modbus server/slave for tower bs_id
    """
    server_man.servers[bs_id - 1].start()


def stop_slave(bs_id):
    """
    Stop modbus server/slave for tower bs_id
    """
    server_man.servers[bs_id - 1].stop()

def stop_server():
    """
    Stop server/slave and logging
    """
    print("[MODBUS_SLAVE] Slave is shutting down ...")
    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_SLAVE] Slave is shutting down ..."
    logger.log(0,log)
    print(log)
    #server.stop()
    for i in range(6):
        stop_slave(i)
    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    print("[MODBUS_SLAVE] Slave is offline")
    log = f"({time_string})-[MODBUS_SLAVE] Slave is offline"
    logger.log(0,log)
    print(log)


def check_power(bs_id):
    """
    Server/slave reads coils containing BS statuses from databank
    """
    server = server_man.servers[bs_id - 1]

    slave_data = class_handler.slave_data_handler(server.data_bank)
    srv_info = server.ServerInfo()
    bs_coil_pow = slave_data.read_coils(1, 1, srv_info)

    return bs_coil_pow

def check_antenna_power(bs_id):
    """
    Server/slave reads coils containing antenna statuses from databank
    """
    server = server_man.servers[bs_id - 1]

    slave_data = class_handler.slave_data_handler(server.data_bank)
    srv_info = server.ServerInfo()
    bs_antenna_pow = slave_data.read_coils(2, 4, srv_info)
    return bs_antenna_pow

def check_gain(bs_id):
    """
    Read gain from modbus server/slave of tower with id 'bs_id'
    """
    server = server_man.servers[bs_id - 1]

    slave_data = class_handler.slave_data_handler(server.data_bank)
    srv_info = server.ServerInfo()
    bs_gain_data = slave_data.read_h_regs(GAIN_ADDR_REG,1,srv_info)

    return bs_gain_data
