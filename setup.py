#!/usr/bin/python

from setuptools import setup, find_packages

install_requires = \
    [
        'uvloop>=0.9.1',
        'websockets>=4.0.1',
        'signalr-client-aio'
    ]

setup(
    name='bittrex_websocket',
    version='0.0.0.1',
    author='Stanislav Lazarov',
    author_email='s.a.lazarov@gmail.com',
    license='MIT',
    dependency_links=['https://github.com/slazarov/python-signalr-client/tarball/master#egg=signalr-client-aio'],
    url='https://github.com/slazarov/python-bittrex-websocket-aio',
    packages=find_packages(exclude=['tests*']),
    install_requires=install_requires,
    description='The unofficial Python websocket (AsyncIO) client for the Bittrex Cryptocurrency Exchange',
    download_url='https://github.com/slazarov/python-bittrex-websocket-aio.git',
    keywords=['bittrex', 'bittrex-websocket', 'orderbook', 'trade', 'bitcoin', 'ethereum', 'BTC', 'ETH', 'client',
              'websocket', 'exchange', 'crypto', 'currency', 'trading', 'async', 'aio'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
