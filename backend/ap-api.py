#!/usr/bin/python3

import asyncio
import json
import logging
import subprocess as sp
import time
from datetime import datetime
from logging import handlers

import pandas as pd
import websockets

from iw_parser import parse_station_dump


async def handler(websocket):
    while True:
        data = await websocket.recv()
        data = json.loads(data)

        if 'type' not in data:
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
        process = sp.Popen(command.split(
            ' '), stdout=sp.PIPE, stderr=sp.STDOUT)
        return process.stdout.read().decode('ascii').replace('\n', '')

    def pi_uptime():
        command = 'uptime -s'
        process = sp.Popen(command.split(
            ' '), stdout=sp.PIPE, stderr=sp.STDOUT)
        data = process.stdout.read().decode('ascii').replace('\n', '')
        return datetime.timestamp(datetime.strptime(data, '%Y-%m-%d %H:%M:%S'))

    def ap_uptime():
        command = 'systemctl show hostapd --property=ActiveEnterTimestamp --value'
        process = sp.Popen(command.split(
            ' '), stdout=sp.PIPE, stderr=sp.STDOUT)
        data = process.stdout.read().decode('ascii').replace('\n', '')
        return datetime.timestamp(datetime.strptime(data, '%a %Y-%m-%d %H:%M:%S %Z'))

    def clients():
        command = 'iw dev wlan0 station dump | grep Station | wc -l'.split(
            ' | ')
        iw = sp.Popen(command[0].split(' '), stdout=sp.PIPE, stderr=sp.STDOUT)
        grep = sp.Popen(command[1].split(
            ' '), stdin=iw.stdout, stdout=sp.PIPE, stderr=sp.STDOUT)
        wc = sp.Popen(command[2].split(
            ' '), stdin=grep.stdout, stdout=sp.PIPE, stderr=sp.STDOUT)
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
    data = [parse_station_dump(device) for device in data]

    return json.dumps({
        'timestamp': time.time() * 1000,
        'type': 'info',
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


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    logger = logging.getLogger('websockets')
    logger.setLevel(logging.WARN)
    logger.addHandler(logging.handlers.RotatingFileHandler(
        "ap-websocket.log", maxBytes=10_000_000, backupCount=2, encoding='UTF-8'))
    asyncio.run(main())
