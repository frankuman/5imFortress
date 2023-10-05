import scada.modbus_tk.defines as cst
import scada.modbus_tk.modbus_tcp as modbus_tcp


master = modbus_tcp.TcpMaster(host="0.0.0.0", port=502)
master.set_timeout(1.0)


def test_read_coils(function_code, starting_address, quantity_of_x):
    """
    Objective: Test if we can extract the expected bits from a slave using the modbus protocol.
    """

    # create READ_COILS request
    actual_bits = master.execute(
        slave=13,
        function_code=function_code,
        starting_address=starting_address,
        quantity_of_x=quantity_of_x
    )
    # the test template sets all bits to 1 in the range 1-128
    # expected_bits = [1 for b in range(0, 128)]
    print(actual_bits)


def test_write_read_coils(function_code, starting_address, output_value):
    """
    Objective: Test if we can change values using the modbus protocol.
    """

    master.execute(
        slave=13,
        function_code=function_code,
        starting_address=starting_address,
        output_value=output_value,
    )

print("Level")
test_read_coils(4, 3000, 7)
# set_bits = [0 for b in range(0, 7)]
# test_write_read_coils(16, 3000, set_bits)
# test_read_coils(4, 3000, 7)
print("Temp")
test_read_coils(4, 3008, 11)
print("Pressure")
test_read_coils(4, 3020, 32)

print("Level/Fill:")
test_read_coils(3, 4000, 7)
set_bits = [0 for b in range(0, 7)]
test_write_read_coils(16, 4000, set_bits)
print("Level/Fill rewritten:")
test_read_coils(3, 4000, 7)
print("Draine")
test_read_coils(3, 4008, 7)