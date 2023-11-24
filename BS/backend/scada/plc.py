"""
This file connects PLC to modbus server/slave
"""
from time import sleep
import json
from BS.backend.api import handler
from BS.backend.helpers import slave_data_handler as slave_handler
from BS.backend.scada import modbus_slave as slave

POWER_ADDR_COIL = 1
BITRATE_ACTIVE_ADDR_REG = 1
BITRATE_TOTAL_ADDR_REG = 5
USERS_ADDR_REG = 9
GAIN_ADDR_REG = 11

import json
from time import sleep

def plc_loop():
    """
    PLC constantly checks status bits for change
    and writes new information from sensors to appropriate registers
    """
    while True:
        # Sleep for 0.5 seconds to control loop frequency
        sleep(0.5)
        
        # Lists to store data from sensors
        coils = []
        gains = []
        antenna_status = []

        # Retrieve data from sensors for each tower
        for i in range(1, 6):
            coil = slave.check_power(i)
            coils.append(coil[0])
            gain = slave.check_gain(i)
            gains.append(gain[0])
            antenna = slave.check_antenna_power(i)
            antenna_status.append(antenna)

        # Check for changes in sensor data and update memory
        check_for_changes([1, 2, 3, 4, 5], coils, gains, antenna_status)

        # Update sensor registers for each tower
        for bs_id in range(1, 6):
            sensors(bs_id)

def sensors(bs_id):
    """
    Updates registers with data from sensors
    """
    # Update registers for bitrate and users
    sensor_bitrate(bs_id)
    sensor_users(bs_id)

def sensor_bitrate(bs_id):
    """
    Sensor for bitrate
    """
    # Gets bitrate via handler
    bitrate_list = handler.get_bitrate(bs_id)

    index = 0
    for i, br in enumerate(bitrate_list):
        if i == 0:
            bitrate_addr = BITRATE_ACTIVE_ADDR_REG
        else:
            bitrate_addr = BITRATE_TOTAL_ADDR_REG

        while br > 0:
            if br > 2**16 - 1:
                # Write bitrate to registers in chunks of 2^16 - 1
                slave_handler.plc_data_handler().write_i_regs(bs_id, bitrate_addr, [2**16 - 1])
                br = br - 2**16 + 1
            else:
                slave_handler.plc_data_handler().write_i_regs(bs_id, bitrate_addr, [br])
                br = br - br
            bitrate_addr += 1
            index += 1
        
        # Fill remaining registers with 0
        if index < 4:
            for i in range(4 - index):
                slave_handler.plc_data_handler().write_i_regs(bs_id, bitrate_addr + i, [0])
    return True

def sensor_users(bs_id):
    """
    Sensor for users
    """
    # Get user count via "handler" file
    users = handler.get_users(bs_id)
    user_addr = USERS_ADDR_REG
    index = 0

    # Write user count to registers in chunks of 2^16 - 1
    while users > 0:
        if users > 2**16 - 1:
            slave_handler.plc_data_handler().write_i_regs(bs_id, user_addr, [2**16 - 1])
            users = users - 2**16 + 1
        else:
            slave_handler.plc_data_handler().write_i_regs(bs_id, user_addr, [users])
            users = users - users
        user_addr = user_addr + 1
        index += 1

    # Fill remaining registers with 0
    if index < 2:
        for i in range(2 - index):
            slave_handler.plc_data_handler().write_i_regs(bs_id, user_addr + i, [0])
    return True

def check_for_changes(bs_addr, coil_info, gain_info, antenna_info):
    """
    Compares status bits with memory to check for changes
    If there are changes, update memory and change BS status via "handler" file
    """
    addr_list = []
    bit_value_list = []
    gain_value_list = []
    antenna_value_list = []

    # Load memory data from JSON file
    with open("BS/backend/scada/plc_mem.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # Extract relevant data from memory
    for item in json_data:
        for output_coil in item.get("output_coil", []):
            addr_list.append(output_coil.get("addr", None))
            bit_value_list.append(output_coil.get("bit_value", None))
            gain_value_list.append(output_coil.get("gain", None))
            antenna_value_list.append(output_coil.get("antenna_pow", None))

    # Check if coil_addr and addr have the same bit values, then check if coil bit has changed
    for j in bs_addr:
        i = j - 1
        if bs_addr[i] == addr_list[i] and coil_info[i] != bit_value_list[i]:
            print("PLC stopped power for id", i)
            handler.change_tower_status(i + 1)
            json_data[i]["output_coil"][0]["bit_value"] = int(coil_info[i])

        if bs_addr[i] == addr_list[i] and gain_info[i] != gain_value_list[i]:
            print("Changing gain for", i, "to", gain_info[i])
            handler.change_gain(i + 1, gain_info[i])
            json_data[i]["output_coil"][0]["gain"] = int(gain_info[i])

        if bs_addr[i] == addr_list[i] and antenna_info[i] != antenna_value_list[i]:
            for k in range(len(antenna_info[i])):
                if antenna_info[i][k] != antenna_value_list[i][k]:
                    print("BS ID:", j, "Antenna index:", k, "status:", antenna_info[i][k])
                    handler.change_antenna_pow(j, k)
                    json_data[i]["output_coil"][0]["antenna_pow"][k] = int(antenna_info[i][k])

    # Update memory with the new data
    with open("BS/backend/scada/plc_mem.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

def reset_mem():
    """
    Reset memory json file to default
    """
    # Load default memory data from JSON file
    with open("BS/backend/scada/plc_mem.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # Reset coil and gain values to default in memory
    for i in range(len(json_data)):
        json_data[i]["output_coil"][0]["bit_value"] = int(True)
        json_data[i]["output_coil"][0]["gain"] = int(0)
        for k in range(4):
            json_data[i]["output_coil"][0]["antenna_pow"][k] = int(1)

    # Save the updated memory data
    with open("BS/backend/scada/plc_mem.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)
