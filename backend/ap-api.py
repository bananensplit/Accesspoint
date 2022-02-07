#!/usr/bin/python3

import argparse
import asyncio
import json
import logging
import re
import subprocess as sp
import time
from argparse import RawTextHelpFormatter
from asyncio import exceptions
from datetime import datetime
from functools import cache
from logging import handlers

import pandas as pd
import websockets

MAC_FILE = ""


async def handler(websocket):
    try:
        while True:
            data = await websocket.recv()
            data = json.loads(data)

            if 'type' not in data or data['type'] not in ("info", "on", "off", "clients_info"):
                await websocket.send(hello_world())
                continue

            if data['type'] == "info":
                await websocket.send(info())
            elif data['type'] == "on":
                await websocket.send(turn_on())
            elif data['type'] == "off":
                await websocket.send(turn_off())
            elif data['type'] == "clients_info":
                await websocket.send(clients_info())
    except websockets.exceptions.ConnectionClosedOK:
        pass


def hello_world():
    return json.dumps({
        'timestamp': time.time() * 1000,
        'type': 'HelloWorld',
        'data': {
            'message': "Hello World!"
        }
    })


def info():
    def ap_state():
        command = 'systemctl is-active hostapd'
        process = sp.Popen(command.split(' '), stdout=sp.PIPE, stderr=sp.STDOUT)
        return process.stdout.read().decode('ascii').replace('\n', '')

    def pi_uptime():
        command = 'uptime -s'
        process = sp.Popen(command.split(' '), stdout=sp.PIPE, stderr=sp.STDOUT)
        data = process.stdout.read().decode('ascii').replace('\n', '')
        return datetime.timestamp(datetime.strptime(data, '%Y-%m-%d %H:%M:%S'))

    def ap_uptime():
        command = 'systemctl show hostapd --property=ActiveEnterTimestamp --value'
        process = sp.Popen(command.split(' '), stdout=sp.PIPE, stderr=sp.STDOUT)
        data = process.stdout.read().decode('ascii').replace('\n', '')
        return datetime.timestamp(datetime.strptime(data, '%a %Y-%m-%d %H:%M:%S %Z'))

    def clients():
        command = 'iw dev wlan0 station dump | grep Station | wc -l'.split(' | ')
        iw = sp.Popen(command[0].split(' '), stdout=sp.PIPE, stderr=sp.STDOUT)
        grep = sp.Popen(command[1].split(' '), stdin=iw.stdout, stdout=sp.PIPE, stderr=sp.STDOUT)
        wc = sp.Popen(command[2].split(' '), stdin=grep.stdout, stdout=sp.PIPE, stderr=sp.STDOUT)
        return int(wc.stdout.read().decode('ascii').replace('\n', ''))

    return json.dumps({
        'timestamp': time.time() * 1000,
        'type': 'info',
        'data': {
            'ap-state': ap_state(),
            'pi-uptime': pi_uptime(),
            'ap-uptime': ap_uptime(),
            'clients': clients(),
        }
    })


def clients_info():
    command = 'iw dev wlan0 station dump'
    iw = sp.Popen(command.split(' '), stdout=sp.PIPE, stderr=sp.STDOUT)
    data = iw.stdout.read().decode('ascii').strip("Station").split("Station")
    data = [parse_station_dump(device) for device in data if device is not None and device != '']

    return json.dumps({
        'timestamp': time.time() * 1000,
        'type': 'clients_info',
        'data': data
    })


def turn_on():
    command = 'sudo systemctl start hostapd'
    process = sp.Popen(command.split(' '), stdout=sp.PIPE, stderr=sp.STDOUT)
    process.communicate()
    return json.dumps({
        'timestamp': time.time() * 1000,
        'type': 'on',
        'data': {
            'success': process.returncode == 0
        }
    })


def turn_off():
    command = 'sudo systemctl stop hostapd'
    process = sp.Popen(command.split(' '), stdout=sp.PIPE, stderr=sp.STDOUT)
    process.communicate()
    return json.dumps({
        'timestamp': time.time() * 1000,
        'type': 'off',
        'data': {
            'success': process.returncode == 0
        }
    })


def parse_station_dump(output):
    lines = output.strip("\n").split("\n")
    mac_address = re.search(r'([0-9a-fA-F]:?){12}', lines[0]).group()

    lines = [re.sub(r"\s", "", line) for line in lines[1:]]
    lines = [line.split(":") for line in lines]
    lines = {line[0]: line[1] for line in lines}

    return {
        'mac': mac_address,
        'vendor': get_vendor_name(mac_address),
        'rx-bitrate': lines["rxbitrate"],
        'tx-bitrate': lines["txbitrate"],
        'connected-time': lines["connectedtime"][:-7],
    }


@cache
def get_mac_addresses(file):
    return pd.read_csv(file, sep=";", encoding_errors='ignore')


@cache
def get_vendor_name(mac_address):
    """
        mac_address format:
            AA-BB-CC-DD-EE-FF
            AA:BB:CC:DD:EE:FF
    """
    macs = get_mac_addresses(MAC_FILE)
    mac = re.sub(r"[-:]", "", mac_address)[0:6].upper()
    erg = macs.loc[macs["Assignment"] == mac, "Organization Name"].values
    return erg[0] if len(erg) >= 0 else None


async def main(port):
    async with websockets.serve(handler, "", port):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    # Argparse
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("-l", "--log-file", type=str, default="ap-api.log", help="logfile path (defaults to ap-api.log)")
    parser.add_argument("-c", "--log-to-console", action="store_true", help="if set will also log to console (and file)")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Determines the verbosity of the log file\n  -v     info (default)\n  -vv    debug")
    parser.add_argument("-p", "--port", type=int, default=8001, help="Port for the websocket (defaults to 8001)")
    parser.add_argument("-m", "--mac-file", type=str, default="resources/mac_addresses_28-01-2022.csv", help="macfile path (defaults to resources/mac_addresses_28-01-2022.csv)")
    args = parser.parse_args()

    # Logging
    logger = logging.getLogger('websockets')

    if args.verbose <= 1:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 2:
        logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    if args.log_to_console:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)

    fileHandler = logging.handlers.RotatingFileHandler(args.log_file, maxBytes=10_000_000, backupCount=2, encoding='UTF-8')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    # Set Mac_file
    MAC_FILE = args.mac_file

    asyncio.run(main(args.port))
