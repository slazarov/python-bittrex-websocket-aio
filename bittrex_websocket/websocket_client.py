#!/usr/bin/python
# -*- coding: utf-8 -*-

# bittrex_websocket/websocket_client.py
# Stanislav Lazarov

import logging
from ._logger import add_stream_logger, remove_stream_logger
from threading import Thread
from ._queue_events import *
from ._constants import EventTypes, BittrexParameters, BittrexMethods, ErrorMessages
from ._auxiliary import process_message, BittrexConnection
from ._abc import WebSocket
from queue import Queue
from ._exceptions import *
from signalr_aio import Connection

logger = logging.getLogger(__name__)


class BittrexSocket(WebSocket):

    def __init__(self):
        self.socket_loop = None
        self.control_queue = None
        self.invokes = []
        self.tickers = None
        self.connection = None
        self.threads = []
        self._start_main_thread()

    def _start_main_thread(self):
        self.control_queue = Queue()
        self.control_queue.put(ConnectEvent())
        thread = Thread(target=self.control_queue_handler, daemon=True, name='ControlQueue')
        self.threads.append(thread)
        thread.start()

    def control_queue_handler(self):
        while True:
            event = self.control_queue.get()
            if event is not None:
                if event.type == EventTypes.CONNECT:
                    self._handle_connect()
                elif event.type == EventTypes.SUBSCRIBE:
                    self._handle_subscribe(event.tickers, event.invoke)
                elif event.type == EventTypes.CLOSE:
                    self.connection.conn.close()
                self.control_queue.task_done()

    def _handle_connect(self):
        connection = Connection(BittrexParameters.URL)
        hub = connection.register_hub(BittrexParameters.HUB)
        connection.received += self._on_debug
        connection.error += self.on_error
        hub.client.on(BittrexParameters.MARKET_DELTA, self._on_public)
        hub.client.on(BittrexParameters.SUMMARY_DELTA, self._on_public)
        hub.client.on(BittrexParameters.SUMMARY_DELTA_LITE, self._on_public)
        # Future implementations
        # hub.client.on(BittrexParameters.BALANCE_DELTA, self._on_private)
        # hub.client.on(BittrexParameters.ORDER_DELTA, self._on_private)
        self.connection = BittrexConnection(connection, hub)
        thread = Thread(target=self._connection_handler, daemon=True, name='SocketConnection')
        self.threads.append(thread)
        thread.start()

    def _connection_handler(self):
        try:
            logger.info('Establishing connection to Bittrex.')
            self.connection.conn.start()
        except ConnectionClosed:
            logger.info('Bittrex connection successfully closed.')

    def _handle_subscribe(self, tickers, invoke):
        if tickers is None:
            self.invokes.append({'invoke': invoke, 'ticker': None})
            self.connection.corehub.server.invoke(invoke)
        else:
            for ticker in tickers:
                self.invokes.append({'invoke': invoke, 'ticker': ticker})
                self.connection.corehub.server.invoke(invoke, ticker)

    # ==============
    # Public Methods
    # ==============

    def subscribe_to_exchange_deltas(self, tickers):
        if type(tickers) is list:
            invoke = BittrexMethods.SUBSCRIBE_TO_EXCHANGE_DELTAS
            event = SubscribeEvent(tickers=tickers, invoke=invoke)
            self.control_queue.put(event)
        else:
            raise TypeError(ErrorMessages.INVALID_TICKER_INPUT)

    def subscribe_to_summary_deltas(self):
        invoke = BittrexMethods.SUBSCRIBE_TO_SUMMARY_DELTAS
        event = SubscribeEvent(tickers=None, invoke=invoke)
        self.control_queue.put(event)

    def subscribe_to_summary_lite_deltas(self):
        invoke = BittrexMethods.SUBSCRIBE_TO_SUMMARY_LITE_DELTAS
        event = SubscribeEvent(tickers=None, invoke=invoke)
        self.control_queue.put(event)

    def query_summary_state(self):
        invoke = BittrexMethods.QUERY_SUMMARY_STATE
        event = SubscribeEvent(tickers=None, invoke=invoke)
        self.control_queue.put(event)

    def query_exchange_state(self, tickers):
        if type(tickers) is list:
            invoke = BittrexMethods.QUERY_EXCHANGE_STATE
            event = SubscribeEvent(tickers, invoke=invoke)
            self.control_queue.put(event)
        else:
            raise TypeError(ErrorMessages.INVALID_TICKER_INPUT)

    def disconnect(self):
        self.control_queue.put(CloseEvent())

    # =======================
    # Private Channel Methods
    # =======================

    async def _on_public(self, args):
        await self.on_public(await process_message(args[0]))

    async def _on_private(self, args):
        ### TO BE IMPLEMENTED ###
        pass

    async def _on_debug(self, **kwargs):
        # `QueryExchangeState` and `QuerySummaryState` are received in the debug channel.
        await self._is_query_invoke(kwargs)

    async def _is_query_invoke(self, kwargs):
        if 'R' in kwargs and type(kwargs['R']) is not bool:
            msg = await process_message(kwargs['R'])
            if msg is None:
                return
            elif 'M' in msg:
                msg['invoke_type'] = BittrexMethods.QUERY_EXCHANGE_STATE

                # Missing ticker name workaround.
                # Fixed in https://github.com/Bittrex/beta/issues/6.
                # Leaving just in case.
                # msg['M'] = self.invokes[int(kwargs['I'])]['ticker']

            else:
                msg['invoke_type'] = BittrexMethods.QUERY_SUMMARY_STATE
            await self.on_public(msg)

    # ======================
    # Public Channel Methods
    # ======================

    async def on_public(self, msg):
        pass

    async def on_private(self, args):
        pass

    async def on_error(self, args):
        pass

    # =============
    # Other Methods
    # =============

    @staticmethod
    def enable_log(file_name=None):
        """
        Enables logging.
        :param file_name: The name of the log file, located in the same directory as the executing script.
        :type file_name: str
        """
        add_stream_logger(file_name=file_name)

    @staticmethod
    def disable_log():
        """
        Disables logging.
        """
        remove_stream_logger()
