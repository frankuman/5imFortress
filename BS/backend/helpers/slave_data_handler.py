"""
Classes to handle data stored with the modbustcp server/slave
"""
from pyModbusTCP.server import DataHandler, ModbusServer, DataBank
import json
class slave_data_handler(DataHandler):
    """
    Custom data handler class
    """
    def read_coils(self, address, count, srv_info):
        return super().read_coils(address, count, srv_info).data

    def read_h_regs(self, address, count, srv_info):
        return super().read_h_regs(address, count, srv_info).data

    # Add functions for other register types if needed

class server_manager:
    """
    Singleton class for sharing the server with other modules

    How to get environment:  server_man = classes.server_manager().instance()
    then environment can be referenced as server_manager.srv
    """
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

            # Get IP addresses and ports of slaves from "config_BS.json"
            with open("BS/config_BS.json", "r", encoding = "utf-8") as f:
                json_data = json.load(f)

            # create new databank for each base station
            data_banks = [DataBank(coils_size=0x10000, coils_default_value = True), 
                          DataBank(coils_size=0x10000, coils_default_value = True),
                          DataBank(coils_size=0x10000, coils_default_value = True), 
                          DataBank(coils_size=0x10000, coils_default_value = True),
                          DataBank(coils_size=0x10000, coils_default_value = True)]
            # create modbus server/slave for each base station
            cls.servers = [ModbusServer(json_data["BS"]["SLAVE1"], json_data["BS"]["PORT1"], no_block = True, data_bank = data_banks[0]),
                           ModbusServer(json_data["BS"]["SLAVE2"], json_data["BS"]["PORT2"], no_block = True, data_bank = data_banks[1]),
                           ModbusServer(json_data["BS"]["SLAVE3"], json_data["BS"]["PORT3"], no_block = True, data_bank = data_banks[2]),
                           ModbusServer(json_data["BS"]["SLAVE4"], json_data["BS"]["PORT4"], no_block = True, data_bank = data_banks[3]),
                           ModbusServer(json_data["BS"]["SLAVE5"], json_data["BS"]["PORT5"], no_block = True, data_bank = data_banks[4])]
            print('Creating new instance')
        return cls._instance

class plc_data_handler():
    """
    Class for data that only the PLC can handle
    i.e some device has measured antenna gain so plc will set the coil itself
    """
    def __init__(self):
        self.slave = server_manager().instance()

    def write_i_regs(self, bs_id, address, words_l):
        """
        Allows the PLC to write to servers/slaves input registers
        """
        return self.slave.servers[bs_id - 1].data_bank.set_input_registers(address, words_l)

    def read_h_regs(self, bs_id, address):
        """
        Allows the PLC to read servers/slave input registers
        """
        return self.slave.servers[bs_id - 1].data_bank.get_holding_registers(address)
