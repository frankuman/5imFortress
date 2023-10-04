#This is a temporary start file
# 21/09/2023
# 5imFortress
from WNS import environment as env
from WNS import util
from WNS import Satellite as sat
from SFclasses import class_environment
import gui.dashboard as dashboard

import numpy as np
import matplotlib.pyplot as plt
import random
import time
import os
import pandas as pd

def setup_env(ue,bs):
    """
    Setup for environment
    """

    #Environment manager for singleton environment
    env_manager = class_environment.EnvironmentManager.instance()

    #Satellite, need multiple base stations, otherwise IGNORE
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
    #
    #bs_6 = env_manager.env1.place_NR_base_station((9000, 9000, 80), 800, 1, 20, 16, 3, 20, 100000)
    #bs.append(bs_6)
    #
    #bs_7 = env_manager.env1.place_NR_base_station((1000, 1000, 40), 800, 1, 20, 16, 3, 20, 100000)
    #bs.append(bs_7)
    #
    #bs_8 = env_manager.env1.place_NR_base_station((9000, 9000, 80), 800, 1, 20, 16, 3, 20, 100000)
    #bs.append(bs_8)

    #5G user equipment, 1 per base station, sat bs
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

    # ue6 = env_manager.env1.insert_ue(1, (9000, 9000, 1), 10000)
    # ue.append(ue6)
    # ue7 = env_manager.env1.insert_ue(1, (1000, 1000, 1), 5000)
    # ue.append(ue7)
    # ue8 = env_manager.env1.insert_ue(1, (9000, 9000, 1), 10000)
    # ue.append(ue8)
    
    env_manager.env1.initial_timestep()
    return True
    
def main():
    
    # env1 = env.wireless_environment(4000, sampling_time = 0.1)

    not_done = True
    ue = []
    bs = []
    error = []
    latency = {}
    prbs = {}
    bitrates = {}
    setup_env(ue,bs)
    env_man = class_environment.EnvironmentManager().instance()
    dashboard.app.run()
    
if __name__ == "__main__":
    main()
