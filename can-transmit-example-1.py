#!/usr/bin/env python3

'''
Python example for sending a message on a CAN bus using python-can.

Example developed on a BeagleBone Black running Debian 10.

Author: Kevin Partin
Email: kevin dot partin at gmail dot com
'''

import can

bus = can.Bus(channel='can0', interface='socketcan', bitrate=125000)
bus.flush_tx_buffer()
msg = can.Message(data=[1, 2, 3, 4, 5, 6, 7, 8])
print(msg)
bus.send(msg)
bus.shutdown()
