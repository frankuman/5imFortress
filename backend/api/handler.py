#This is a temporary start file
# 21/09/2023
# 5imFortress
"""
This file connects the WNS simulation backend to the PLC
"""

from backend.simulation import util
from backend.helpers import class_environment

def change_tower_status(id):
    """
    Stops the tower with id (if tower is do, it will go down)
    """
    env_man = class_environment.environment_manager().instance()
    tower_status = env_man.env1.all_bs_list[id].bs_change_status()
    print("TOWER ID: " + str(id) + " STATUS: " + tower_status)
    env_man.env1.next_timestep()
    return tower_status

def get_bitrate(id):
    """
    Return allocated bitrate and total bitrate of tower by id.
    Gets called every 2 seconds by dashboard
    """
    bs = util.find_bs_by_id(id)
    ue_id = bs.get_connected_users()
    if ue_id is None:
        return [0, 0]
    util.find_ue_by_id(ue_id).update_connection()
    if bs.bs_status() == "UP":
        bitlist = [int(bs.allocated_bitrate), int(bs.total_bitrate)]
    else:
        bitlist = [0, 0]
    env_man = class_environment.environment_manager().instance()
    env_man.env1.next_timestep()

    return bitlist

def get_users(id):
    """
    Return number of users connected to bs 'id'.
    Called by dashboard
    """
    bs = util.find_bs_by_id(id)
    ue_id = bs.get_connected_users()
    if ue_id is None:
        return 0
    util.find_ue_by_id(ue_id).update_connection()
    if bs.bs_status() == "UP":
        users = util.find_ue_by_id(ue_id).get_users()
    else:
        users = 0
    env_man = class_environment.environment_manager().instance()
    env_man.env1.next_timestep()
    return users

def change_gain(id, gain):
    """
    Change antenna_gain of base station
    In parameter change_gain(id, gain)
    """
    bs = util.find_bs_by_id(id)
    bs.change_gain(gain)
    return True

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
