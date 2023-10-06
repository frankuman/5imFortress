from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform

def start_server():
    # Create an instance of ModbusServer
    server = ModbusServer("127.0.0.1", 502, no_block=True)

    try:
        print("Start server...")
        server.start()

        print("Server is online")
        #state = [0]
        while True:
            print("")
            sleep(3)
            re = server.data_bank.get_coils(1)
            print(re)
            if re:
                pass
            
                #PLC.change_power(1)
        #     DataBank.set_words(0, [int(uniform(0, 100))])
        #     if state != DataBank.get_words(1):
        #         state = DataBank.get_words(1)
        #         print("Value of Register 1 has changed to " +str(state))
        #     sleep(0.5)
    except:
        print("Shutdown server ...")
        server.stop()
        print("Server is offline")