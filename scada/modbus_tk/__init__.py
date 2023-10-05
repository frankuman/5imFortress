#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Modbus TestKit: Implementation of Modbus protocol in python

 (C)2009 - Luc Jean - luc.jean@gmail.com
 (C)2009 - Apidev - http://www.apidev.fr

 This is distributed under GNU LGPL license, see license.txt

 Make possible to write modbus TCP and RTU master and slave for testing purpose
 Modbus TestKit is different from pymodbus which is another implementation of
 the modbus stack in python

contributors:
----------------------------------
* OrangeTux
* denisstogl
* MELabs
* idahogray
* riaan.doorduin
* tor.sjowall
* smachin1000
* GadgetSteve 
* dhoomakethu
* zerox1212
* ffreckle
* Matthew West
* Vincent Prince
* kcl93
* https://github.com/Slasktra
* travijuu
* Jackson Matheson
* SushiTee
Please let us know if your name is missing!

"""

import logging

logging.basicConfig(filename='datalogger/logs/system_log.txt', level=logging.INFO, filemode='w')
LOGGER = logging.getLogger("modbus_tk")


VERSION = '1.1.3'
