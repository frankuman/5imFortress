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
import scada.modbus_master as modbus_master



def start_tower(id,env1):
    """
    Starts the tower with id (if tower is up, it will go down)
    """
    print(env1.all_bs_list[id].bs_change_status())
    env1.next_timestep()

def stop_tower(id,env1):
    """
    Stops the tower with id (if tower is do, it will go down)
    """
    
    tower_status = env1.all_bs_list[id].bs_change_status()
    print("TOWER ID: "+str(id)+" STATUS: "+tower_status)
    #if tower_status == "UP":
        #util.find_ue_by_id(id).connect_to_bs_id(id)
    env1.next_timestep()
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
    bs = util.find_bs_by_id(id)
    ue_id = bs.get_connected_users()
    if ue_id == None:
        return [0,0]
    util.find_ue_by_id(ue_id).update_connection()
    if bs.bs_status() == "UP":
        bitlist = [int(bs.allocated_bitrate), int(bs.total_bitrate)]
    else:
        bitlist = [0,0]
    env_man = class_environment.EnvironmentManager().instance()
    env_man.env1.next_timestep()
    modbus_master.write_coil()
    return bitlist

    ## Tower 1 UP    42/100
    ## Tower 2 UP   51/60
    ## Tower 3 DOWN 0/100

def get_users(id):
    """
    Return number of users connected to bs 'id'.
    Called by dashboard
    """
    bs = util.find_bs_by_id(id)
    ue_id = bs.get_connected_users()
    if ue_id == None:
        return 0
    util.find_ue_by_id(ue_id).update_connection()
    if bs.bs_status() == "UP":
        users = util.find_ue_by_id(ue_id).get_users()
    else:
        users = 0
    env_man = class_environment.EnvironmentManager().instance()
    env_man.env1.next_timestep()
    return users

def move_ue(id):
    pass

def status(env1):
    """
    Prints out all of the general information for towers
    """
    for bs in env1.all_bs_list:
        if bs.bs_type == "nr":
            print("Basestation with ID: ", bs.bs_id)
            print("status: ", bs.bs_status())
            for ele in bs.bs_properties().keys():
                print("     ", ele, ": ", bs.bs_properties()[ele])