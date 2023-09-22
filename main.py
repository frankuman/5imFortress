#This is a temporary start file
# 21/09/2023
# 5imFortress
from WNS import environment as env
from WNS import util
from WNS import Satellite as sat
import dashboard

import numpy as np
import matplotlib.pyplot as plt
import random
import time
import os
import pandas as pd



class EnvironmentManager:
    """
    Singleton class for sharing the enviroment with other modules

    How to get environment:  env_man = main.EnvironmentManager().instance()
    then environment can be referenced as env_man.env1
    """
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            cls.env1 = env.wireless_environment(4000, sampling_time = 0.1)
        return cls._instance
    
def setup_env(ue,bs):
    """
    Setup for environment
    """
    env_manager = EnvironmentManager.instance()

    sat_bs = env_manager.env1.place_SAT_base_station(10000, (1000, 2000))
    bs.append(sat_bs)
    bs_1 = env_manager.env1.place_NR_base_station((2000, 2000, 40), 800, 1, 20, 16, 3, 20, 1000)
    bs.append(bs_1)
    bs_2 = env_manager.env1.place_NR_base_station((4000, 4000, 80), 800, 1, 20, 16, 3, 20, 1000)
    bs.append(bs_2)
    ue0 = env_manager.env1.insert_ue(0, (2000, 2000, 1), 0, 100) #Has id 0
    ue.append(ue0)
    ue1 = env_manager.env1.insert_ue(1, (2000, 2000, 1), 0, 100)
    ue.append(ue1)
    ue2 = env_manager.env1.insert_ue(1, (4000, 4000, 1), 0, 100)
    ue.append(ue2)
    #ue3 = env_manager.env1.insert_ue(1, (2000, 2000, 1), 1, 5)
    # 
    env_manager.env1.initial_timestep()

    
    util.find_ue_by_id(1).connect_to_bs_id(1)
    util.find_ue_by_id(2).connect_to_bs_id(2)
    #util.find_ue_by_id(2).connect_to_bs_id(2)

    env_manager.env1.next_timestep()
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
    env_man = EnvironmentManager().instance()
    dashboard.app.run()
    # while not_done: #Temporary menu. Only stop_tower works
    #     print("Bitrate: ", util.find_bs_by_id(1).allocated_bitrate)
    #     print("Bitrate UE: ", util.find_ue_by_id(0).bs_bitrate_allocation)

    #     print("--------------\nChoose a option")
    #     print("1. Start tower: (id)")
    #     print("2. Shut down tower: (id)")
    #     print("3. Disconnect UE: (id)")
    #     print("4. Connect UE: (id)")
    #     print("5. Show UE connectivity")
    #     print("6. Show tower status/info/signals/id")
    #     print("7. Move UE")
    #     print("8. Print overall status")

    #     command = input(">> ")
    #     if command not in "12345678":
    #         print("Invalid command")
    #     elif command == "1":
    #         start_tower(1,env_man.env1)
    #     elif command == "2":
    #         stop_tower(1, env_man.env1)
    #     elif command == "3":
    #         pass
    #     elif command == "4":
    #         pass
    #     elif command == "5":
    #         pass
    #     elif command == "6":
    #         pass
    #     elif command == "7":
    #         pass
    #     elif command == "8":
    #         status(env_man.env1)

def start_tower(id,env1):
    """
    Starts the tower with id (if tower is up, it will go down)
    """
    print(env1.all_bs_list[id].bs_change_status())
    env1.next_timestep()

def stop_tower(id,env1): #"IndexError: pop index out of range" if pressed to many times too fast
    """
    Stops the tower with id (if tower is do, it will go down)
    """
    
    tower_status = env1.all_bs_list[id].bs_change_status()
    print("TOWER ID: "+str(id)+" STATUS: "+tower_status)
    if tower_status == "UP":
        util.find_ue_by_id(id).connect_to_bs_id(id)
    return(tower_status)

# BS 1 -> UE 1
# BS 2 -> UE 2
# BS 3 -> UE 3
def disconnect_ue(ue_id, bs_id):
    util.find_ue_by_id(ue_id).disconnect_from_bs(bs_id)

def connect_ue(ue_id, bs_id):
    util.find_ue_by_id(ue_id).connect_to_bs_id(bs_id)

def show_connection(id):
    pass

def show_bs_status(id):
    pass
def get_bitrate(id):
    """
    Return allocated bitrate and total bitrate of tower by id.
    Gets called every 2 seconds by dashboard
    """
    ue = util.find_bs_by_id(id).get_connected_users()
    for i in ue:
        util.find_ue_by_id(i).update_connection()
    bs = util.find_bs_by_id(id)
    if bs.bs_status() == "UP":
        bitlist = [bs.allocated_bitrate, bs.total_bitrate]
    else:
        bitlist = [0,0]
    env_man = EnvironmentManager().instance()

    env_man.env1.next_timestep()
    return bitlist

    ## Tower 1 UP    42/100
    ## Tower 2 UP   51/60
    ## Tower 3 DOWN 0/100
def move_ue(id):
    pass

def status(env1):
    """
    Prints out all of the general information for towers
    """
    for bs in env1.all_bs_list:
        if bs.bs_type == "nr":
            print("Basestation with ID: ", bs.bs_id)
            print(" status: ", bs.bs_status())
            for ele in bs.bs_properties().keys():
                print("     ", ele, ": ", bs.bs_properties()[ele])

if __name__ == "__main__":
    main()
