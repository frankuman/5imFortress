"""
This file connects modbus communicates with modbus client/master via modbustcp protocol
"""
import datetime
from pyModbusTCP.server import DataBank
from backend.helpers import slave_data_handler as class_handler
from frontend.datalogger import logger

#Initiate data_bank for server, with all coils as 1
#to make sure all towers start with status UP
data_bank = DataBank(coils_size=0x10000, coils_default_value = True)
#Create modbus server to use for towers
server = class_handler.server_manager().instance()
server = server.srv

def start_server():
    """"
    Start modbus server and loop for updating status coils
    """
    # try:
    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_SLAVE] Slave starting on 127.0.0.1:502"
    logger.log(0,log)
    #log = "Starting slave..."

    server.start()
    print("[MODBUS_SLAVE] Server is online")
    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_SLAVE] Server is online"
    logger.log(0,log)


def stop_server():
    """
    Stop server/slave and logging
    """
    print("[MODBUS_SLAVE] Slave is shutting down ...")
    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    log = f"({time_string})-[MODBUS_SLAVE] Slave is shutting down ..."
    logger.log(0,log)
    server.stop()
    current_time = datetime.datetime.now()

    time_string = current_time.strftime('%H:%M:%S')
    print("[MODBUS_SLAVE] Slave is offline")
    log = f"({time_string})-[MODBUS_SLAVE] Slave is offline"
    logger.log(0,log)


def check_power():
    """
    Server/slave reads coils containing BS statuses from databank
    """
    slave_data = class_handler.slave_data_handler(server.data_bank)
    srv_info = server.ServerInfo()

    bs_coil_pow = slave_data.read_coils(1, 5, srv_info)

    return [1,2,3,4,5], bs_coil_pow
