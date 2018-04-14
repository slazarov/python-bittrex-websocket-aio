#!/usr/bin/python
# -*- coding: utf-8 -*-

# bittrex_websocket/examples/account_level_data.py
# Stanislav Lazarov

# Sample script showing how to subscribe to the private callbacks (Balance Delta and Order Delta) of Bittrex.
# You need to provide your api_key and api_secret with the respective permissions.
# For more info check _abc.py or https://github.com/Bittrex/beta


from bittrex_websocket.websocket_client import BittrexSocket
from time import sleep


def main():
    class MySocket(BittrexSocket):

        async def on_private(self, msg):
            print(msg)

    # Create the socket instance
    ws = MySocket()

    # Enable logging
    ws.enable_log()
    ws.authenticate('### API KEY ###', '### API SECRET ###')

    while True:
        sleep(10)


if __name__ == "__main__":
    main()
