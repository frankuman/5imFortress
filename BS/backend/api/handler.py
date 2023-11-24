#This is a temporary start file
# 21/09/2023
# 5imFortress
"""
This file connects the WNS simulation backend to the PLC
"""

from BS.backend.simulation import util
from BS.backend.helpers import class_environment

def change_tower_status(bs_id):
    """
    Stops the tower with id (if tower is UP, it will go DOWN)
    """
    env_man = class_environment.environment_manager().instance()
    tower_status = env_man.env1.all_bs_list[bs_id].bs_change_status()
    print("TOWER ID: " + str(bs_id) + " STATUS: " + tower_status)
    env_man.env1.next_timestep()
    return tower_status

def get_bitrate(bs_id):
    """
    Return allocated bitrate and total bitrate of tower by id.
    Gets called every 2 seconds by dashboard
    """
    bs = util.find_bs_by_id(bs_id)
    ue_id = bs.get_connected_ue()
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

def get_users(bs_id):
    """
    Return number of users connected to bs 'bs_id'.
    Called by dashboard
    """
    bs = util.find_bs_by_id(bs_id)
    ue_id = bs.get_connected_ue()
    if ue_id is None:
        return 0
    util.find_ue_by_id(ue_id).update_connection()
    if bs.bs_status() == "UP":
        users = bs.get_connected_users()
    else:
        users = 0
    env_man = class_environment.environment_manager().instance()
    env_man.env1.next_timestep()
    return users

def change_gain(bs_id, gain):
    """
    Change antenna_gain of base station
    In parameter change_gain(id, gain)
    """
    bs = util.find_bs_by_id(bs_id)
    bs.change_gain(gain)
    return True

def change_antenna_pow(bs_id, antenna_index):
    """
    Change power status of antenna "antenna_index" on base station "bs_id"
    """
    bs = util.find_bs_by_id(bs_id)
    bs.change_antenna_status(antenna_index)
    return True
