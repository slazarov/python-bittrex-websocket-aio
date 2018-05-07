# bittrex-websocket-aio
Asynchronous Python websocket client for getting live streaming data from [Bittrex Exchange](http://bittrex.com).

The library is based on asyncio, hence it requires Python>=3.5.

If you are using lower Python version (2.7 / 3.0 - 3.4) or prefer gevent, try my other library [slazarov/python-bittrex-websocket](https://github.com/slazarov/python-bittrex-websocket)

# My plans for the websocket client

Bittrex released their [official beta websocket documentation](https://github.com/Bittrex/beta) on 27-March-2018.
The major changes were the removal of the need to bypass Cloudflare and the introduction of new public (`Lite Summary Delta`) and private (`Balance Delta` & `Order Delta`) channels.

Following that, I decided to repurpose the client as a higher level Bittrex API which users can use to build on. The major changes, which are going to be reflected both in the aio and soon in the gevent version of the client, will be:

* ~~Existing methods will be restructured in order to mimic the official ones, i.e `subscribe_to_orderbook_update` will become `subscribe_to_exchange_deltas`. This would make referencing the official documentation more clear and will reduce confusion.~~
* ~~`QueryExchangeState` will become a public method so that users can invoke it freely.~~
* The method `subscribe_to_orderbook` will be removed and instead placed as a separate module. Before the latter happens, users can use the legacy library.
* ~~Private, account specific methods will be implemented, i.e `Balance Delta` & `Order Delta`~~
* ~~Replacement of the legacy `on_channels` with only two channels for the public and private streams.~~

### Disclaimer

*I am not associated with Bittrex. Use the library at your own risk, I don't bear any responsibility if you end up losing your money.*

*The code is licensed under the MIT license. Please consider the following message:*
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE

# What can I use it for?
You can use it for various purposes, some examples include:
* maintaining live order book
* recording trade history
* analysing order flow

Use your imagination.

# Notices

# Road map

# Dependencies

# Installation

The library can be installed through Github and PyPi. For the latest updates, use Github.

```python
pip install git+https://github.com/slazarov/python-bittrex-websocket-aio.git
pip install git+https://github.com/slazarov/python-bittrex-websocket-aio.git@next-version-number
pip install bittrex-websocket-aio
```

# Methods
#### Custom URL
Custom URLs can be passed to the client upon instantiating.
```python
# 'https://socket.bittrex.com/signalr' is currently Cloudflare protected
# 'https://beta.bittrex.com/signalr' (DEFAULT) is not

# Create the socket instance
ws = MySocket(url=None)
# rest of your code
```
#### Subscribe Methods
```python
def subscribe_to_exchange_deltas(self, tickers):
    """
    Allows the caller to receive real-time updates to the state of a SINGLE market.
    Upon subscribing, the callback will be invoked with market deltas as they occur.

    This feed only contains updates to exchange state. To form a complete picture of
    exchange state, users must first call QueryExchangeState and merge deltas into
    the data structure returned in that call.

    :param tickers: A list of tickers you are interested in.
    :type tickers: []
    """


def subscribe_to_summary_deltas(self):
    """
    Allows the caller to receive real-time updates of the state of ALL markets.
    Upon subscribing, the callback will be invoked with market deltas as they occur.

    Summary delta callbacks are verbose. A subset of the same data limited to the
    market name, the last price, and the base currency volume can be obtained via
    `subscribe_to_summary_lite_deltas`.

    https://github.com/Bittrex/beta#subscribetosummarydeltas
    """

def subscribe_to_summary_lite_deltas(self):
    """
    Similar to `subscribe_to_summary_deltas`.
    Shows only market name, last price and base currency volume.

    """

def query_summary_state(self):
    """
    Allows the caller to retrieve the full state for all markets.
    """

def query_exchange_state(self, tickers):
    """
    Allows the caller to retrieve the full order book for a specific market.

    :param tickers: A list of tickers you are interested in.
    :type tickers: []
    """

def authenticate(self, api_key, api_secret):
    """
    Verifies a user’s identity to the server and begins receiving account-level notifications

    :param api_key: Your api_key with the relevant permissions.
    :type api_key: str
    :param api_secret: Your api_secret with the relevant permissions.
    :type api_secret: str
    """
```

#### Other Methods

```python
def disconnect(self):
    """
    Disconnects the socket.
    """

def enable_log(file_name=None):
    """
    Enables logging.

    :param file_name: The name of the log file, located in the same directory as the executing script.
    :type file_name: str
    """

def disable_log():
    """
    Disables logging.
    """
```

# Message channels
```python
async def on_public(self, msg):
    # The main channel for all public methods.

async def on_private(self, msg):
    # The main channel for all private methods.

async def on_error(self, error):
    # Receive error message from the SignalR connection.

```

# Sample usage
Check the examples folder.

# Change log
0.0.0.2.5 - 22/04/2018
* Custom urls can now be passed to the client
* If `cfscrape` is installed, the client will automatically use it

0.0.2 - 14/04/2018
* Implemented reconnection
* Implemented private account-level methods. Check `authenticate(self, api_key, api_secret)`.

0.0.1 - 07/04/2018
* Initial release on github.

# Other libraries
**[python-bittrex-autosell](https://github.com/slazarov/python-bittrex-autosell)**

Python CLI tool to auto sell coins on Bittrex.

It is used in the cases when you want to auto sell a specific coin for another, but there is no direct market, so you have to use an intermediate market.

**[python-signalr-client-aio](https://github.com/slazarov/python-signalr-client)**

SignalR client for python based on asyncio

**[bittrex-websocket](https://github.com/slazarov/python-bittrex-websocket)**

Python gevent-based websocket client (SignalR) for getting live streaming data from Bittrex Exchange.
