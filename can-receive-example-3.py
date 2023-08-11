#!/usr/bin/env python3

'''
Python example for receiving a message on a CAN bus using python-can.

Example developed on a BeagleBone Black running Debian 10.

Author: Kevin Partin
Email: kevin dot partin at gmail dot com
'''

import can
import sys

can_id = 0
filters = None

if len(sys.argv) > 1:
    can_id = int(sys.argv[1], 10)
    filters = [{"can_id": can_id, "can_mask": 0x7FF, "extended": False}]

with can.interface.Bus(channel='can0', interface='socketcan', bitrate=125000, can_filters=filters) as bus:
    for msg in bus:
        print(msg)
