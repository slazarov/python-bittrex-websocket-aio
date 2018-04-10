#!/usr/bin/python
# -*- coding: utf-8 -*-

# bittrex_websocket/_abc.py
# Stanislav Lazarov

from abc import ABC, abstractmethod


class WebSocket(ABC):

    @abstractmethod
    def subscribe_to_exchange_deltas(self, tickers):
        """
        Allows the caller to receive real-time updates to the state of a SINGLE market.
        Upon subscribing, the callback will be invoked with market deltas as they occur.

        This feed only contains updates to exchange state. To form a complete picture of
        exchange state, users must first call QueryExchangeState and merge deltas into
        the data structure returned in that call.

        :param tickers: A list of tickers you are interested in.
        :type tickers: []

        https://github.com/Bittrex/beta/#subscribetoexchangedeltas

        JSON Payload:
            {
                MarketName: string,
                Nonce: int,
                Buys:
                    [
                        {
                            Type: string - enum(ADD | REMOVE | UPDATE),
                            Rate: decimal,
                            Quantity: decimal
                        }
                    ],
                Sells:
                    [
                        {
                            Type: string - enum(ADD | REMOVE | UPDATE),
                            Rate: decimal,
                            Quantity: decimal
                        }
                    ],
                Fills:
                    [
                        {
                            OrderType: string,
                            Rate: decimal,
                            Quantity: decimal,
                            TimeStamp: date
                        }
                    ]
            }
        """

    @abstractmethod
    def subscribe_to_summary_deltas(self):
        """
        Allows the caller to receive real-time updates of the state of ALL markets.
        Upon subscribing, the callback will be invoked with market deltas as they occur.

        Summary delta callbacks are verbose. A subset of the same data limited to the
        market name, the last price, and the base currency volume can be obtained via
        `subscribe_to_summary_lite_deltas`.

        https://github.com/Bittrex/beta#subscribetosummarydeltas

        JSON Payload:
            {
                Nonce : int,
                Deltas :
                [
                    {
                        MarketName     : string,
                        High           : decimal,
                        Low            : decimal,
                        Volume         : decimal,
                        Last           : decimal,
                        BaseVolume     : decimal,
                        TimeStamp      : date,
                        Bid            : decimal,
                        Ask            : decimal,
                        OpenBuyOrders  : int,
                        OpenSellOrders : int,
                        PrevDay        : decimal,
                        Created        : date
                    }
                ]
            }
        """

    @abstractmethod
    def subscribe_to_summary_lite_deltas(self):
        """
        Similar to `subscribe_to_summary_deltas`.
        Shows only market name, last price and base currency volume.

        JSON Payload:
            {
                Deltas:
                    [
                        {
                            MarketName: string,
                            Last: decimal,
                            BaseVolume: decimal
                        }
                    ]
            }
        """

    @abstractmethod
    async def on_public(self, msg):
        """
        Streams all incoming messages from public delta channels.
        """

    @abstractmethod
    async def on_private(self, msg):
        """
        Streams all incoming messages from private delta channels.
        """
