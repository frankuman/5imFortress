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
import threading



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
    bs_2 = env_manager.env1.place_NR_base_station((2000, 2000, 40), 800, 1, 20, 16, 3, 20, 1000)
    bs.append(bs_2)
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
    env_man = EnvironmentManager().instance()
    dashboard.app.run()
    while not_done: #Temporary menu. Only stop_tower works
        print("--------------\nChoose a option")
        print("1. Start tower: (id)")
        print("2. Shut down tower: (id)")
        print("3. Disconnect UE: (id)")
        print("4. Connect UE: (id)")
        print("5. Show UE connectivity")
        print("6. Show tower status/info/signals/id")
        print("7. Move UE")
        print("8. Print overall status")

        command = input(">> ")
        if command not in "12345678":
            print("Invalid command")
        elif command == "1":
            start_tower(1,env_man.env1)
        elif command == "2":
            stop_tower(1, env_man.env1)
        elif command == "3":
            pass
        elif command == "4":
            pass
        elif command == "5":
            pass
        elif command == "6":
            pass
        elif command == "7":
            pass
        elif command == "8":
            status(env_man.env1)

def start_tower(id,env1):
    """
    Starts the tower with id (if tower is up, it will go down)
    """
    print(env1.all_bs_list[id].bs_change_status())

def stop_tower(id,env1):
    """
    Stops the tower with id (if tower is do, it will go down)
    """
    tower_status = env1.all_bs_list[id].bs_change_status()
    print("TOWER ID: "+str(id)+" STATUS: "+tower_status)
    return(tower_status)


def disconnect_ue(id):
    pass

def connect_ue(id):
    pass

def show_connection(id):
    pass

def show_bs_status(id):
    pass

def move_ue(id):
    pass

def status(env1):
    """
    Prints out all of the general information for towers
    """
    for i, bs in enumerate(env1.all_bs_list):
        if i != 0:
            print("Basestation with ID: ", i)
            print(" status: ", bs.bs_status())
            for ele in bs.bs_properties().keys():
                print("     ", ele, ": ", bs.bs_properties()[ele])

if __name__ == "__main__":
    main()
