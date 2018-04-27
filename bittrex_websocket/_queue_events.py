#!/usr/bin/python
# -*- coding: utf-8 -*-

# bittrex_websocket/_queue_events.py
# Stanislav Lazarov

from ._constants import EventTypes


class ConnectEvent:
    """
    Handles the event of creating a new connection.
    """

    def __init__(self):
        self.type = EventTypes.CONNECT


class SubscribeEvent:
    """
    Handles the event of subscribing specific ticker(s) to specific channels.
    """

    def __init__(self, invoke, *payload):
        self.type = EventTypes.SUBSCRIBE
        self.invoke = invoke
        self.payload = payload


class CloseEvent:
    """
    Handles the event of closing the socket.
    """

    def __init__(self):
        self.type = EventTypes.CLOSE
