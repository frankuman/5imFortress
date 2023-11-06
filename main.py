#!/usr/bin/env python3
# 21/09/2023
# 5imFortressRelevance 10, Login page , Necessary 10, Achievement 10
"""
Starts backend, WNS and modbus server/slave
"""

from backend.helpers import class_environment
from scada import modbus_slave
from scada import plc
from multiprocessing import Process, Pool
import time
import gui_main

def setup_env(ue, bs):
    """
    Setup for WNS environment
    """
    #Environment manager for singleton environment
    env_manager = class_environment.environment_manager.instance()

    #Satellite, fills out bs list, otherwise IGNORE
    sat_bs = env_manager.env1.place_SAT_base_station(10000, (1000, 2000))
    bs.append(sat_bs)

    #5G base stations
    #Karlskrona
    bs_1 = env_manager.env1.place_NR_base_station((1000, 1000, 40), 800, 1, 20, 16, 3, 20, 250000)
    bs.append(bs_1)
    #Karlshamn
    bs_2 = env_manager.env1.place_NR_base_station((4000, 4000, 40), 800, 1, 20, 16, 3, 20, 100000)
    bs.append(bs_2)
    #Ronneby
    bs_3 = env_manager.env1.place_NR_base_station((7000, 7000, 40), 800, 1, 20, 16, 3, 20, 100000)
    bs.append(bs_3)
    #Soelvesborg
    bs_4 = env_manager.env1.place_NR_base_station((10000, 10000, 40), 800, 1, 20, 16, 3, 20, 100000)
    bs.append(bs_4)
    #Olofstroem
    bs_5 = env_manager.env1.place_NR_base_station((13000, 13000, 40), 800, 1, 20, 16, 3, 20, 100000)
    bs.append(bs_5)

    #5G user equipment, 1 per base station
    #Sat ue, fills out ue list, otherwise IGNORE
    ue_sat = env_manager.env1.insert_ue(1, (10000000, 10000000, 1), 10000) # connects to satellite
    ue.append(ue_sat)

    #Normal user equipment, connecting to base stations
    #Karlskrona
    ue1 = env_manager.env1.insert_ue(1, (1000, 1000, 1), 66000)
    ue.append(ue1)
    #Karlshamn
    ue2 = env_manager.env1.insert_ue(1, (4000, 4000, 1), 19000)
    ue.append(ue2)
    #Ronneby
    ue3 = env_manager.env1.insert_ue(1, (7000, 7000, 1), 12000)
    ue.append(ue3)
    #Soelvesborg    
    ue4 = env_manager.env1.insert_ue(1, (10000, 10000, 1), 8000)
    ue.append(ue4)
    #Olofstroem
    ue5 = env_manager.env1.insert_ue(1, (13000, 13000, 1), 7000)
    ue.append(ue5)

    env_manager.env1.initial_timestep()
    return True

def main():
    """
    Setup backend, WNS environment and modbus server/slave
    """
    #Empty old logs
    for i in "12345":
        filename = "frontend/datalogger/logs/bs_log_" + i + ".txt"
        open(filename, "w", encoding = "utf-8").close()
    filename = "frontend/datalogger/logs/system_lo  g.txt"
    open(filename, "w", encoding = "utf-8").close()

    ue = []
    bs = []

    setup_env(ue, bs)

    env_man = class_environment.environment_manager().instance()
    plc.reset_mem()
    #Remove try and except when debugging
    #try:
    modbus_slave.start_server()
    plc.plc_loop()

    #except:
    modbus_slave.stop_server()

if __name__ == "__main__":
    p1 = Process(target=main)  # Pass a reference to the main function
    p2 = Process(target=gui_main.main)  # Pass a reference to gui_main.main

    p1.start()
    p2.start()

    p1.join()
    p2.join()
