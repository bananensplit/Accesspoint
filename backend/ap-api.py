#!/usr/bin/python3

import asyncio
from datetime import datetime
from logging import handlers
import json
import logging
import subprocess as sp
import time

import websockets


async def handler(websocket):
    while True:
        data = await websocket.recv()
        data = json.loads(data)

        if 'type' not in data:
            await websocket.send(hello_world())
            continuine

        if data['type'] == "info":
            await websocket.send(info())
        elif data['type'] == "on":
            await websocket.send(turn_on())
        elif data['type'] == "off":
            await websocket.send(turn_off())


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
        return 'coming soon!'

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
    logger.addHandler(logging.handlers.RotatingFileHandler("ap-websocket.log", maxBytes=10_000_000, backupCount=2, encoding='UTF-8'))
    asyncio.run(main())
