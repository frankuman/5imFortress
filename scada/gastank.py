# modbus support
#import modbus_tk.defines as cst

# import scada.modbus_tk.defines as cst
# import scada.modbus_tk.modbus_tcp as modbus_tcp

# # connect to modbus
# master = modbus_tcp.TcpMaster(host="0.0.0.0", port=502)
# master.set_timeout(1.0)

# def modbus_write(function_code, starting_address, output_value):
#     master.execute(
#         slave=13,
#         function_code=function_code,
#         starting_address=starting_address,
#         output_value=output_value,
#     )

# def modbus_read(function_code, starting_address, quantity_of_x):
#     # create READ_COILS request
#     actual_bits = master.execute(
#         slave=13,
#         function_code=function_code,
#         starting_address=starting_address,
#         quantity_of_x=quantity_of_x
#     )

#     return actual_bits

# def modbus_read_int(function_code, starting_address, quantity_of_x):  
#     bit_array = modbus_read(function_code, starting_address, quantity_of_x)

#     tmp = ''

#     for x in bit_array:
#         tmp += str(x)

#     return int(tmp,2)

# def modbus_write_int(function_code, starting_address, value):
#     bit_array = []

#     for x in bin(value)[2:]:
#         bit_array.append(int(x))

#     while len(bit_array) < 7:
#         bit_array.insert(0,0)

#     modbus_write(function_code, starting_address, bit_array)   


# class GasTank(object):
#     def __init__(self):
#         self.level = self.get_level()
#         self.temp = self.get_temp()
#         self.pressure = self.get_pressure() 
#         self.maxlevel = 100

#     def fill(self, amount):
#         # fills the tank for a certain amount
#         self.update()  

#         if self.level+amount <= self.maxlevel:
#             self.level += amount
#             modbus_write_int(16,4000,self.level)
#         else:
#             print("amount is too high")

#     def drain(self, amount):
#         # drains the tank for a certain amount
#         self.update() 

#         if self.level-amount >= 0:
#             self.level -= amount
#             modbus_write_int(16,4000,self.level)
#         else:
#             print("amount is too high")

#     def update(self):
#         self.level = self.get_level()
#         self.temp = self.get_temp()
#         self.pressure = self.get_pressure() 

#     def get_level(self):
#         return modbus_read_int(3,4000,7)

#     def get_temp(self):
#         return modbus_read_int(4,3008,11)

#     def get_pressure(self):
#         return modbus_read_int(4,3020,32)              