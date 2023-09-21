import numpy as np
import matplotlib.pyplot as plt
import random
import time
import os
import pandas as pd

import WNS.environment as environment
import WNS.util as util
import WNS.Satellite as Satellite


env = environment.wireless_environment(5,5,400)
ue = []
bs = []
sat_bs = env.place_SAT_base_station(10000, (1000, 2000))
bs.append(sat_bs)
id = env.insert_ue(1, starting_position = (0,0,1), speed = 0, direction = 0)
ue.append(id)

bs_id = env.place_NR_base_station((0,0,50), 800, 2, 20, 16, 6, 100, total_bitrate = 10000)
bs.append(bs_id)

env.initial_timestep();
print(env.wardrop_beta)

phone = ue[0]
util.find_ue_by_id(phone).connect_to_bs_id(0)
env.next_timestep()
# ue_id = 41250 users
BS_POWER = True
counter = 0
while(BS_POWER == True):
    time.sleep(0.5)
    connected_users = env.bs_list[0].get_connected_users()
    print(connected_users)
    counter += 1
    if counter == 5:
        env.bs_list[0].request_disconnection(0)
    if counter == 10:
        util.find_ue_by_id(phone).connect_to_bs_id(0)

