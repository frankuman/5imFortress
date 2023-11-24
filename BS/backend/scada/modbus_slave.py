"""
This file connects modbus communicates with modbus client/master via modbustcp protocol
"""
import datetime
from BS.backend.helpers import slave_data_handler as class_handler
from BS.backend.datalogger import logger

POWER_ADDR_COIL = 1
BITRATE_ACTIVE_ADDR_REG = 1
BITRATE_TOTAL_ADDR_REG = 5
USERS_ADDR_REG = 9
GAIN_ADDR_REG = 11

print('Creating new instance')
server_man = class_handler.server_manager().instance()

import datetime

def start_server():
    """
    Start modbus server and loop for updating status coils
    """
    # Get the current time
    cur_time = datetime.datetime.now()

    # Format the current time as a string
    time_str = cur_time.strftime('%H:%M:%S')

    # Log and print the start message for the Modbus server
    log = f"({time_str})-[MODBUS_SLAVE] Slave starting"
    logger.log(0, log)
    print(log)

    # Start individual servers for each tower
    for i in range(1, 6):
        start_slave(i)

    # Log and print that the Modbus server is online
    print("[MODBUS_SLAVE] Server is online")
    log = f"({time_str})-[MODBUS_SLAVE] Server is online"
    logger.log(0, log)
    print(log)

def start_slave(bs_id):
    """
    Start modbus server/slave for tower bs_id
    """
    # Start the Modbus server for the specified tower
    server_man.servers[bs_id - 1].start()

def stop_slave(bs_id):
    """
    Stop modbus server/slave for tower bs_id
    """
    # Stop the Modbus server for the specified tower
    server_man.servers[bs_id - 1].stop()

def stop_server():
    """
    Stop servers/slaves and logging
    """
    # Log and print that the Modbus slave is shutting down
    print("[MODBUS_SLAVE] Slave is shutting down ...")
    cur_time = datetime.datetime.now()
    time_str = cur_time.strftime('%H:%M:%S')
    log = f"({time_str})-[MODBUS_SLAVE] Slave is shutting down ..."
    logger.log(0, log)
    print(log)

    # Stop all Modbus servers for each tower
    for i in range(6):
        stop_slave(i)

    # Log and print that the Modbus slave is offline
    cur_time = datetime.datetime.now()
    time_str = cur_time.strftime('%H:%M:%S')
    print("[MODBUS_SLAVE] Slave is offline")
    log = f"({time_str})-[MODBUS_SLAVE] Slave is offline"
    logger.log(0, log)
    print(log)

def check_power(bs_id):
    """
    Server/slave reads coils containing BS statuses from databank
    """
    # Get the Modbus server for the specified tower
    server = server_man.servers[bs_id - 1]

    # Create a handler for slave data from the server's databank
    slave_data = class_handler.slave_data_handler(server.data_bank)

    # Get server information
    srv_info = server.ServerInfo()

    # Read coils containing BS statuses from the databank
    bs_coil_pow = slave_data.read_coils(1, 1, srv_info)

    return bs_coil_pow

def check_antenna_power(bs_id):
    """
    Server/slave reads coils containing antenna statuses from databank
    """
    # Get the Modbus server for the specified tower
    server = server_man.servers[bs_id - 1]

    # Create a handler for slave data from the server's databank
    slave_data = class_handler.slave_data_handler(server.data_bank)

    # Get server information
    srv_info = server.ServerInfo()

    # Read coils containing antenna statuses from the databank
    bs_antenna_pow = slave_data.read_coils(2, 4, srv_info)
    return bs_antenna_pow

def check_gain(bs_id):
    """
    Read gain from modbus server/slave of tower with id 'bs_id'
    """
    # Get the Modbus server for the specified tower
    server = server_man.servers[bs_id - 1]

    # Create a handler for slave data from the server's databank
    slave_data = class_handler.slave_data_handler(server.data_bank)

    # Get server information
    srv_info = server.ServerInfo()

    # Read gain from the Modbus server/slave
    bs_gain_data = slave_data.read_h_regs(GAIN_ADDR_REG, 1, srv_info)

    return bs_gain_data
