#!/usr/bin/env python3
# 21/09/2023
# 5imFortressRelevance 10, Login page , Necessary 10, Achievement 10
"""
Starts backend, WNS and modbus server/slave
"""

from BS.backend.helpers import class_environment
from BS.backend.scada import modbus_slave
from BS.backend.scada import plc
import time
import socket

def setup_env():
    """
    Setup for WNS environment
    """
    #Environment manager for singleton environment
    env_manager = class_environment.environment_manager.instance()

    #Satellite, fills out bs list, just IGNORE
    env_manager.env1.place_SAT_base_station(10000, (1000, 2000))

    #5G base stations
    #Karlskrona
    env_manager.env1.place_NR_base_station((1000, 1000, 40), 800, 1, 20, 0, 3, 20, 250000, 4)
    #Karlshamn
    env_manager.env1.place_NR_base_station((4000, 4000, 40), 800, 1, 20, 0, 3, 20, 100000, 4)
    #Ronneby
    env_manager.env1.place_NR_base_station((7000, 7000, 40), 800, 1, 20, 0, 3, 20, 100000, 4)
    #Soelvesborg
    env_manager.env1.place_NR_base_station((10000, 10000, 40), 800, 1, 20, 0, 3, 20, 100000, 4)
    #Olofstroem
    env_manager.env1.place_NR_base_station((13000, 13000, 40), 800, 1, 20, 0, 3, 20, 100000, 4)

    #5G user equipment, 1 per base station
    #Sat ue, fills out ue list, just IGNORE
    env_manager.env1.insert_ue(1, (10000000, 10000000, 1), 10000) # connects to satellite

    #Normal user equipment, connecting to base stations
    #Karlskrona
    env_manager.env1.insert_ue(1, (1000, 1000, 1), 66000)
    #Karlshamn
    env_manager.env1.insert_ue(1, (4000, 4000, 1), 19000)
    #Ronneby
    env_manager.env1.insert_ue(1, (7000, 7000, 1), 12000)
    #Soelvesborg
    env_manager.env1.insert_ue(1, (10000, 10000, 1), 8000)
    #Olofstroem
    env_manager.env1.insert_ue(1, (13000, 13000, 1), 7000)

    env_manager.env1.initial_timestep()
    return True

def main():
    """
    Setup backend, WNS environment and modbus server/slave
    """

    #Empty old logs
    for i in "12345":
        filename = "BS/backend/datalogger/logs/bs_log_" + i + ".txt"
        open(filename, "w", encoding = "utf-8").close()
    filename = "BS/backend/datalogger/logs/system_log.txt"
    open(filename, "w", encoding = "utf-8").close()

    #Add default BS and UE to environment and do initial_timestep
    setup_env()

    plc.reset_mem()
    #Remove try and except when debugging
    try:
        modbus_slave.start_server()
        plc.plc_loop()
    except:
        modbus_slave.stop_server()

if __name__ == "__main__":
    main()
