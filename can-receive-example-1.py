#!/usr/bin/env python3

'''
Python example for receiving a message on a CAN bus using python-can.

Example developed on a BeagleBone Black running Debian 10.

Author: Kevin Partin
Email: kevin dot partin at gmail dot com
'''

import can

bus = can.Bus(channel='can0', interface='socketcan', bitrate=125000)
msg = bus.recv()
print(msg)
bus.shutdown()
