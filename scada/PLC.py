"""
This file connects PLC to modbus server/slave
"""
from time import sleep
import json
from backend.api import handler
from backend.helpers import slave_data_handler as slave_handler
from scada import modbus_slave as slave

def plc_loop():
    """
    PLC constantly checks status bits for change
    and writes new information from sensors to appropriate registers
    """
    while True:
        sleep(0.5)
        addr, coil = slave.check_power()
        addr.sort()
        check_if_coil_pow_changed(addr, coil)
        for bs_id in range(1, 6):
            sensors(bs_id)

def sensors(bs_id):
    """
    Updates registers with data from sensors
    """
    sensor_bitrate(bs_id)
    sensor_users(bs_id)

def sensor_bitrate(bs_id):
    """
    Sensor for bitrate
    """
    #gets bitrate via "handler" file
    bitrate_list = handler.get_bitrate(bs_id)
    #Bitrate address is between 0-48
    index = 0
    for i, br in enumerate(bitrate_list):
        bitrate_addr = (bs_id - 1) * 8 + i * 4
        while br > 0:
            if br > 2**16 - 1:
                slave_handler.plc_data_handler().write_i_regs(bitrate_addr, [2**16 - 1])

                br = br - 2**16 + 1
            else:
                slave_handler.plc_data_handler().write_i_regs(bitrate_addr, [br])
                br = br - br
            bitrate_addr = bitrate_addr + 1
            index += 1
        if index < 4:
            for i in range(4 - index):
                slave_handler.plc_data_handler().write_i_regs(bitrate_addr + i, [0])
    return True

def sensor_users(bs_id):
    """
    Sensor for users
    """
    users = handler.get_users(bs_id)
    user_addr = 100 + (bs_id - 1) * 2
    index = 0
    while users > 0:
        if users > 2**16 - 1:
            slave_handler.plc_data_handler().write_i_regs(user_addr, [2**16 - 1])
            users = users - 2**16 + 1
        else:
            slave_handler.plc_data_handler().write_i_regs(user_addr, [users])
            users = users - users
        user_addr = user_addr + 1
        index += 1
    if index < 2:
        for i in range(2 - index):
            slave_handler.plc_data_handler().write_i_regs(user_addr + i, [0])
    return True

def check_if_coil_pow_changed(coil_addr,coil_info):
    """
    Compares status bits with memory to check for changes
    If there are changes, update memory and change BS status via "handler" file
    """
    addr_list = []
    bit_value_list = []
    with open("scada/plc_mem.json", "r", encoding = "utf-8") as f:
        json_data = json.load(f)

    for item in json_data:
        for output_coil in item.get("output_coil", []):
            addr_list.append(output_coil.get("addr", None))
            bit_value_list.append(output_coil.get("bit_value", None))

    # Check if coil_addr and addr have the same bit values, then check if coil bit has changed
    for i in range(len(coil_addr)):
        if coil_addr[i] == addr_list[i] and coil_info[i] != bit_value_list[i]:
            print("PLC stoppped power for id", i)
            handler.change_tower_status(i + 1)
            json_data[i]["output_coil"][0]["bit_value"] = int(coil_info[i])

    with open("scada/plc_mem.json", "w", encoding = "utf-8") as f:
        json.dump(json_data, f, indent = 4)

def reset_mem():
    """
    Reset memory json file to default
    """
    with open("scada/plc_mem.json", "r", encoding = "utf-8") as f:
        json_data = json.load(f)

    #print(json_data)
    # Check if coil_addr and addr have the same bit values, then check if coil bit has changed
    for i in range(len(json_data)):
        #print(json_data[0].get('output_coil')[0])
        json_data[i]["output_coil"][0]["bit_value"] = int(True)

    with open("scada/plc_mem.json", "w", encoding = "utf-8") as f:
        json.dump(json_data, f, indent = 4)
