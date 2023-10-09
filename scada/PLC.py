from time import sleep
from random import uniform
import json
import api.dashboard_handler as handler
import scada.modbus_slave as slave
import scada.slave_data_handler as slave_handler

def plc_loop():
    while True:
        sleep(1)
        addr, coil = slave.check_power()
        gather_coil_info(addr, coil)
        for id in range(1, 6):
            sensors(id)

def sensors(id):
    bitrate_list = handler.get_bitrate(id)

    # [201956, 250000]
    # i = 0
    # br = 201956
    # 65535 on addr 12416
    # br = 136421
    # addr = 12432
    # 65535 on addr 12432
    # br = 70886
    # addr = 12448
    # br = 5351
    # addr = 12464
    #----
    # i = 1
    # br = 250000
    #print("Bitrate List:", bitrate_list)
    for i, br in enumerate(bitrate_list):
        #bitrate_addr = 12288 + id * 128 + i * 16
        bitrate_addr = id * 8 + i * 4
        while br > 0:
            if br > 2**16 - 1:
                slave_handler.plc_data_handler().write_i_regs(bitrate_addr, [2**16 - 1])

                br = br - 2**16 + 1
            else:
                slave_handler.plc_data_handler().write_i_regs(bitrate_addr, [br])
                br = br - br
            bitrate_addr = bitrate_addr + 1

    #bitrate = bitrate
    #Calculate address for bitrate register
    #0x3000 and 128 bits for each
    # bitrate_addr = 12288 + id * 128
    # slave_handler.plc_data_handler().write_i_regs(bitrate_addr, [bitrate_list[0]])
    # bitrate_addr = 12288 + id * 128 + 64
    # slave_handler.plc_data_handler().write_i_regs(bitrate_addr, [bitrate_list[1]])

def gather_coil_info(coil_addr, coil_info):
    coil_addr.sort()
    check_if_coil_pow_changed(coil_addr,coil_info)


def check_if_coil_pow_changed(coil_addr,coil_info):

    addr_list = []
    bit_value_list = []
    with open("scada/plc_mem.json", "r") as f:
        json_data = json.load(f)

    for item in json_data:
        for output_coil in item.get("output_coil", []):
            addr_list.append(output_coil.get("addr", None))
            bit_value_list.append(output_coil.get("bit_value", None))
    #print(json_data)
    # Check if coil_addr and addr have the same bit values, then check if coil bit has changed
    for i in range(len(coil_addr)):
        if coil_addr[i] == addr_list[i] and coil_info[i] != bit_value_list[i]:
           print("PLC stoppped power for id", i)
           handler.stop_tower(i+1)
           #print(json_data[0].get('output_coil')[0])
           json_data[i]["output_coil"][0]["bit_value"] = int(coil_info[i])
           #
    with open("scada/plc_mem.json", "w") as f:
        json.dump(json_data, f, indent = 4)

def reset_mem():
    with open("scada/plc_mem.json", "r") as f:
        json_data = json.load(f)

    #print(json_data)
    # Check if coil_addr and addr have the same bit values, then check if coil bit has changed
    for i in range(len(json_data)):
           #print(json_data[0].get('output_coil')[0])
           json_data[i]["output_coil"][0]["bit_value"] = int(True)
           #
    with open("scada/plc_mem.json", "w") as f:
        json.dump(json_data, f, indent = 4)
