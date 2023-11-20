import pyModbusTCP
import pyModbusTCP.client as client

TARGETS = []
def main():
    modbus_scan("192.168.0.")
    print(TARGETS)

def modbus_scan(net):

    #Recon
    for ip in range(108,111):
        for targetport in range(500,507):
            target = net+str(ip)
            print(target+":"+str(targetport))
            client1 = client.ModbusClient(host = target, port = targetport, auto_open = True, auto_close = False, timeout = 0.5)
            state = client1.open()
            if state:
                print("Found opening")
                TARGETS.append((target,str(targetport)))

if __name__ == "__main__":
    main()