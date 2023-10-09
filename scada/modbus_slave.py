
from time import sleep
from random import uniform

from pyModbusTCP.server import ModbusServer, DataBank, DataHandler
import scada.PLC as plc
import scada.slave_data_handler as class_handler
from datalogger import logger
import datetime

#Initiate data_bank for server, with all bits as 1
#to make sure all towers start with status UP
data_bank = DataBank(coils_size=0x10000, coils_default_value = True)
#Create modbus server to use for towers
server = ModbusServer("127.0.0.1", 502, no_block=True,data_bank=data_bank)

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
    #state = [0]
    #check_slaves()
    

def stop_server():

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
    slave_data = class_handler.slave_data_handler(server.data_bank)
    srv_info = server.ServerInfo()

    bs_coil_pow = slave_data.read_coils(1, 5, srv_info)

    return [1,2,3,4,5], bs_coil_pow

    # bs_coil_pow = slave_data.read_d_inputs(1, 5, srv_info)
    # print("BS_COIL_POW = ", bs_coil_pow)


    # bs_coil_pow = server.data_bank.get_coils(1, 5, srv_info)
    # print("BS_COIL_POW = ", bs_coil_pow)

    # bs_reg_pow = server.data_bank.get_holding_registers(14, 1)
    # print("BS_COIL_POW = ", bs_reg_pow)
    #plc.gather_coil_info([1, 2, 3, 4, 5], bs_coil_pow)


