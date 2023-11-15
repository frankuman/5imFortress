"""
Classes to handle data stored with the modbustcp server/slave
"""
from pyModbusTCP.server import DataHandler, ModbusServer, DataBank

class slave_data_handler(DataHandler):
    """
    Custom data handler class
    """
    #Class for data that slave can handle itself
    def read_coils(self, address, count, srv_info):
        return super().read_coils(address, count, srv_info).data
        #return DataBank.get_coils(address,count, srv_info)

    # def read_d_inputs(self, address, count, srv_info):
    #     return super().read_d_inputs(address, count, srv_info)

    def read_h_regs(self, address, count, srv_info):
        return super().read_h_regs(address, count, srv_info).data

    # def read_i_regs(self, address, count, srv_info):
    #     return super().read_i_regs(address, count, srv_info)

    # def write_h_regs(self, address, words_l, srv_info):
    #     return super().write_h_regs(address, words_l, srv_info)

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
            data_banks = [DataBank(coils_size=0x10000, coils_default_value = True), DataBank(coils_size=0x10000, coils_default_value = True),
                          DataBank(coils_size=0x10000, coils_default_value = True), DataBank(coils_size=0x10000, coils_default_value = True),
                          DataBank(coils_size=0x10000, coils_default_value = True)]
            cls.servers = [ModbusServer("192.168.0.200", 502, no_block = True, data_bank = data_banks[0]),ModbusServer("192.168.0.201", 502, no_block = True, data_bank = data_banks[1]),
                           ModbusServer("192.168.0.202", 502, no_block = True, data_bank = data_banks[2]),ModbusServer("192.168.0.203", 502, no_block = True, data_bank = data_banks[3]),
                           ModbusServer("192.168.0.204", 502, no_block = True, data_bank = data_banks[4])]
            print('Creating new instance')

            # data_bank = DataBank(coils_size=0x10000, coils_default_value = True)
            # cls.srv = ModbusServer("127.0.0.1", 502, no_block = True, data_bank = data_bank)
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
