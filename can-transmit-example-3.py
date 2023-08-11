#!/usr/bin/env python3

'''
Python example for sending a message on a CAN bus using python-can.

Example developed on a BeagleBone Black running Debian 10.

Author: Kevin Partin
Email: kevin dot partin at gmail dot com
'''

import can
import sys

can_id = 0

if len(sys.argv) > 1:
    can_id = int(sys.argv[1], 10)

with can.Bus(channel='can0', interface='socketcan', bitrate=125000) as bus:
    bus.flush_tx_buffer()
    msg = can.Message(arbitration_id=can_id, is_extended_id=False, data=[1, 2, 3, 4, 5, 6, 7, 8])
    bus.send(msg)
