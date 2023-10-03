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
    bs_1 = env_manager.env1.place_NR_base_station((1000, 1000, 40), 800, 1, 20, 16, 3, 20, 100000)
    bs.append(bs_1)
    bs_2 = env_manager.env1.place_NR_base_station((9000, 9000, 80), 800, 1, 20, 16, 3, 20, 100000)
    bs.append(bs_2)

    #5G user equipment, 1 per base station
    ue0 = env_manager.env1.insert_ue(1, (10000000, 10000000, 1), 10000) # connects to satellite
    ue.append(ue0)
    #Normal user equipment, connecting to base stations
    ue1 = env_manager.env1.insert_ue(1, (1000, 1000, 1), 5000)
    ue.append(ue1)
    ue2 = env_manager.env1.insert_ue(1, (9000, 9000, 1), 10000)
    ue.append(ue2)
    
    env_manager.env1.initial_timestep()

    #util.find_ue_by_id(1).connect_to_bs_id(1)
    #util.find_ue_by_id(2).connect_to_bs_id(2)
    #util.find_ue_by_id(2).connect_to_bs_id(2)

    #env_manager.env1.next_timestep()
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
