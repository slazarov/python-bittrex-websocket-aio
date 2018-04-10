#!/usr/bin/python
# -*- coding: utf-8 -*-

# bittrex_websocket/_auxiliary.py
# Stanislav Lazarov

import logging
from uuid import uuid4

try:
    from pybase64 import b64decode
except:
    from base64 import b64decode
from zlib import decompress, MAX_WBITS

try:
    from ujson import loads
except:
    from json import loads

logger = logging.getLogger(__name__)


async def process_message(message):
    try:
        deflated_msg = decompress(b64decode(message, validate=True), -MAX_WBITS)
    except SyntaxError:
        deflated_msg = decompress(b64decode(message, validate=True))
    return loads(deflated_msg.decode())


class BittrexConnection(object):
    def __init__(self, conn, hub):
        self.conn = conn
        self.corehub = hub
        self.id = uuid4().hex
