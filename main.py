#This is a temporary start file
# 21/09/2023
# 5imFortress
from  WNS import environment
from WNS import util
from WNS import Satellite as sat
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import os
import pandas as pd


def main():
    env = environment.wireless_environment(4000, sampling_time = 0.1)
    ue = []
    bs = []
    error = []
    latency = {}
    prbs = {}
    bitrates = {}
    sat_bs = env.place_SAT_base_station(10000, (1000, 2000))
    bs.append(sat_bs)
    bs_1 = env.place_NR_base_station((2000, 2000, 40), 800, 1, 20, 16, 3, 20, 1000)
    bs.append(bs_1)
    env.initial_timestep()
    not_done = True
    while not_done:
        print("--------------\nChoose a option")
        print("1. Start tower: (id)")
        print("2. Shut down downer: (id)")
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
            pass
        elif command == "2":
            pass
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
            pass

def start_tower(id):
    pass
def stop_tower(id):
    pass
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
def status():
    #Prints the status for all towers and their ID
    pass

if __name__ == "__main__":
    main()

