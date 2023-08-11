#!/usr/bin/env python3

'''
Python example for using a listener, callback and a notifier on a CAN bus 
using python-can.

Example developed on a BeagleBone Black running Debian 10.

Author: Kevin Partin
Email: kevin dot partin at gmail dot com
'''

import asyncio
import can
from typing import Any, Callable


class MessageListener(can.Listener):
    '''
    Simple CAN listener
    '''
    
    def __init__(self, callback: Callable[[can.Message], None], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.is_stopped: bool = False
        self.__callback = callback

    def on_message_received(self, msg: can.Message) -> None:
        if not self.is_stopped:
            self.__callback(msg)
    
    def stop(self) -> None:
        self.is_stopped = True


class Connection:


    def __init__(self, bus, callback, filter: int = None, extended: bool = False):
        '''
        Create a CAN bus connection'''

        self.__bus = bus
        self.__extended = extended
        self.__mask = 0x1fffffff if extended else 0x7ff

        listener = MessageListener(callback)

        self.__notifier = can.Notifier(bus=self.__bus, listeners=[listener], timeout=0)

        if filter:
            self.addFilter(filter)


    def addCallback(self, callback):
        '''
        Adds a callback (via an additional listener) to the notifier attached to this bus.
        '''

        # Create a new listener for the callback.
        listener = MessageListener(callback)

        # Add the listener to the notifier.
        self.__notifier.add_listener(listener)


    def addFilter(self, can_id: int = 0):
        '''
        Adds a filter to the CAN bus to allow messages with the specified
        `can_id` to be passed to the callback(s).
        '''
        # Retrieve a list of the current CAN bus filters.
        filters = self.__bus.filters

        # Add the new filter to the list.
        if filters:
            filters.append({"can_id": can_id, "can_mask": self.__mask, "extended": self.__extended})
        else:
            filters = [{"can_id": can_id, "can_mask": self.__mask, "extended": self.__extended}]

        # Update the filters for the CAN bus.
        self.__bus.set_filters(filters)


    def deleteFilter(self, can_id: int = 0):
        '''
        Deletes a filter from the CAN bus. Removes the filter with the specified `can_id`.
        '''
        filters = []

        for filter in self.__bus.filters:
            if filter['can_id'] != can_id:
                filters.append(filter)

        # Update the filters for the CAN bus.
        self.__bus.set_filters(filters)


    def send(self, can_id, data):
        '''
        Send the data over CAN bus using the connection
        '''
        msg = can.Message(arbitration_id=can_id, extended_id=self.__extended, data=data)
        self.__bus.send(msg)


def callback(msg: can.Message) -> None:
    print(msg)

bus = can.interface.Bus(channel='can0', interface='socketcan', bitrate=125000)
connection = Connection(bus, callback, 3)

loop = asyncio.new_event_loop()

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

bus.shutdown()
