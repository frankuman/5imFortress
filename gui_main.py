#!/usr/bin/env python3
import gui.dashboard as dashboard
import scada.modbus_master as modbus_master
def main():
    modbus_master.start_client()
    dashboard.app.run(debug=True)

if __name__ == "__main__":
    main()
