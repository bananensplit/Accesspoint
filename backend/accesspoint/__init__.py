#!/usr/bin/python3
import asyncio
import json
import threading
import time
from datetime import datetime, timedelta

import websockets

from accesspoint.Accesses import Accesses
from accesspoint.GeneralInfo import GeneralInfo
from accesspoint.ReadLog import ReadLog
from accesspoint.Uptime import Uptime


async def client_handler(websocket, path):
    while True:
        request = await websocket.recv()

        if request.lower() == 'chartdata':
            with threading.Lock():
                global data_cache
                await websocket.send(f'{{"data": {json.dumps(data_cache)} }}')

        if request.lower() == 'generalinfo':
            generalinfo.update_general_info()
            await websocket.send(f'{{"data": {json.dumps(generalinfo.get_as_dict())} }}')


def start_websocket():
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(client_handler, "192.168.0.100", 3000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def update_data(interval=5):
    while True:
        start = datetime.now().date() - timedelta(14)
        end = datetime.now().date()

        uptime.update_uptimes()

        accesses.update_accesses()

        uptime_data = uptime.get_as_list(start, end)
        accesses_data = accesses.get_number_accesses(start, end)

        erg = []
        for i in range(0, len(uptime_data)):
            if uptime_data[i]['date'] != accesses_data[i]['date']:
                return -1

            erg.append({
                'date': uptime_data[i]['date'],
                'ap-actions': uptime_data[i]['ap-actions'],
                'rp-actions': uptime_data[i]['rp-actions'],
                'accesses': accesses_data[i]['accesses']
            })

        with threading.Lock():
            global data_cache
            data_cache = erg

        time.sleep(interval)


def main():
    global uptime, accesses, generalinfo
    uptime = Uptime()
    # accesses = Accesses(ReadLog('../Resources/new', 'other_vhosts_access\\.log.*'), '.*:2000')
    accesses = Accesses(ReadLog('/var/log/apache2', 'other_vhosts_access\\.log.*'), '.*:2000')
    generalinfo = GeneralInfo()

    thread1 = threading.Thread(target=start_websocket)
    thread2 = threading.Thread(target=update_data, args=(5,))
    thread1.start()
    thread2.start()


uptime = None
accesses = None
generalinfo = None
data_cache = None

if __name__ == '__main__':
    main()
