#!/usr/bin/env python3

'''
Python example for sending a message on a CAN bus using python-can.

Example developed on a BeagleBone Black running Debian 10.

Author: Kevin Partin
Email: kevin dot partin at gmail dot com
'''

import can
import time

with can.interface.Bus(channel='can0', interface='socketcan', bitrate=125000) as bus: 
	bus.flush_tx_buffer()
	for can_id in range(1, 11):
		msg = can.Message(timestamp=time.time(), arbitration_id=can_id, data=[1, 2, 3, 4, 5, 6, 7, 8], is_extended_id=False)
		print(msg)
		bus.send(msg)
		time.sleep(0.5)
