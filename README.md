# 5imFortress - A 5G Infrastructure Attack Simulation

![5imFortress Logo](https://github.com/frankuman/5imFortress/blob/main/docs/images/type5-banner-big.png?raw=true)

## Team Members
- [Oliver Bölin](https://github.com/frankuman)
- [Farhad Asadi](https://github.com/frhd143)
- [Kim Budischewski](https://github.com/LostNeverKnown)
- [Michael Törnvall](https://github.com/Mickelito)

## Project Overview
5imFortress is an ongoing IT security project developed as part of a university course at Blekinge Tekniska Högskola (BTH). The project revolves around creating a realistic simulation for 5G towers in Blekinge Län, Sweden. These towers are controlled by an HMI ModBus Server, allowing modifications to the hardware of the 5G towers. Additionally, the project includes an example attack on the ModBus server, simulating a breach attempt to test the security of 5G tower systems.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Usage Examples](#usage-examples)
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
  
## Requirements
- Python 3.7.0 or higher
- Pip
- Two virtual machines (1 for HMI, and 1 for BS - basestation)
- Network connection is preferred for images and map but not needed.

## Installation
1. Download the required files for each virtual machine either using git or manual download.
2. Choose the virtual machine for simulating the HMI and the one for the BS, delete unnecessary folders accordingly.
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

## Usage Examples

### Dashboard: Map and Status
The dashboard provides an overview of the 5G towers' geographical positions and their current status. It displays the number of connected User Equipment (UE) and provides information on factors affecting connectivity, such as gain, bitrate, and other relevant metrics.

<img src="https://github.com/frankuman/5imFortress/assets/57047010/83ffa5a7-ea6a-46c8-8ec1-8a68d69fb34a" width="400">

### HMI: Power Button and Bitrate
In the HMI interface, you can monitor the overall power status of the Base Stations (BS) and their respective bitrates. The power button allows you to toggle the entire BS on or off, disconnecting all associated UEs.

<img src="https://github.com/frankuman/5imFortress/assets/57047010/8082c966-3c76-436a-a433-c82f1901a729" width="400">

### Antenna Power Button
This feature enables you to activate individual antennas, each affecting approximately 25% of the tower's output in their respective directions. The selector allows you to choose which tower to modify.

<img src="https://github.com/frankuman/5imFortress/assets/57047010/4a26553d-e692-4348-b218-e43e071064f4" width="400">

### Selector
The selector tool allows you to choose the specific tower you want to modify, providing a targeted approach to adjustments.

<img src="https://github.com/frankuman/5imFortress/assets/57047010/5f550281-a1db-43b1-8f74-1ec287f9d216" width="400">

### Gain Slider
Adjust the gain slider to fine-tune the tower's gain, ranging from 0% to 100%. Higher gain results in directional antennas, concentrating the coverage area into a smaller point. This allows for maximizing bitrate in a specific area, albeit limiting the number of users who can access it.

<img src="https://github.com/frankuman/5imFortress/assets/57047010/5b379886-d139-4c55-ba95-d03edb399f33" width="100">

### Graph
The graph provides a visual representation of the bitrate for each tower over the last 30 seconds, offering insights into performance trends.
 
<img src="https://github.com/frankuman/5imFortress/assets/57047010/28c96570-b8ab-4816-87c7-6dd1e12dcb29" width="400">

Feel free to explore these features to optimize the performance and configuration of the 5G towers within the system.

### GigaAttacker

#### Attack commands coming soon!

## Known Issues
Known issues will be presented here

Issue 1:

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

## Roadmap (currently in sprint 3)
Sprint 1:

✅ F1: Simulate 5G Base Station (basic)

✅ F2: SCADA HMI (basic)

✅ F3: Simulate User Equipment (basic)

✅ F4: Simulate Base Station SCADA

✅ F5: Dashboard Map of Base Stations

✅ F6: View All Base Stations’ Info

✅ F9: Notifications (log)

✅ F12: Simulation Dashboard (basic)

✅ (Bonus): Login page

🟡 (Testing & Finetuning)

Sprint 2:

✅ F7: HMI (advanced)

✅ F8: Simulate 5G Base Station (advanced)

✅ (Bonus): Login page for HMI

🟡 (Testing & Finetuning)

Sprint 3:

❌ F10: Documentation

❌ F11: Launch Attack on SCADA Server

❌ F13: Simulation Dashboard (advanced)

## Contact
- You can contact the project team at [olbo20@student.bth.se](mailto:olbo20@student.bth.se).

Thank you
![image](https://github.com/frankuman/5imFortress/assets/57047010/e38ef278-6752-4180-b719-d2c6a14b61b0)
(Farhad does not meet the team standard (he is sent to gulag))
