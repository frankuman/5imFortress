from pyModbusTCP.server import DataHandler, ModbusServer, DataBank
#server = ModbusServer("127.0.0.1", 502, no_block=True)

class slave_data_handler(DataHandler):
    """
    Custom data handler class
    """
    #Class for data that slave can handle itself
    def read_coils(self, address, count, srv_info):
        return super().read_coils(address, count, srv_info).data
        #return DataBank.get_coils(address,count, srv_info)

    def read_d_inputs(self, address, count, srv_info):
        return super().read_d_inputs(address, count, srv_info)


    def read_h_regs(self, address, count, srv_info):
        return super().read_h_regs(address, count, srv_info)


    def read_i_regs(self, address, count, srv_info):
        return super().read_i_regs(address, count, srv_info)

    def write_h_regs(self, address, words_l, srv_info):
        return super().write_h_regs(address, words_l, srv_info)

    # def _write_i_regs(self, address, words_l):
    #     #can only be used from plc_data_handler, i.e the slave cant use this function
    #     super().data_bank.set_input_registers(self, address=address,word_list=words_l)
    #     return DataBank.set_input_registers(DataBank,address=address,word_list=words_l)
    #     return super().set_input_registers()
    #     pass
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
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            data_bank = DataBank(coils_size=0x10000, coils_default_value = True)
            cls.srv = ModbusServer("127.0.0.1", 502, no_block = True, data_bank = data_bank)
        return cls._instance
          
class plc_data_handler():#->Farhad
    #Class for data that only the PLC can handle, i.e some device has measured antenna gain so plc will set the coil itself

    # id1 = 3001
    #
    #
    #
    #
    #
    
    def __init__(self):
        
        self.slave = server_manager().instance()
        self.slave = self.slave.srv

    def write_i_regs(self, address, words_l):
        return self.slave.data_bank.set_input_registers(address, words_l)

    