#!/usr/bin/python3
from datetime import datetime, timedelta

from accesspoint.Accesses import Accesses
from accesspoint.Uptime import Uptime


def get_data(days_back=14):
    now = datetime.now().date()
    uptime = Uptime()
    uptime_data = uptime.get_as_list(now - timedelta(days_back - 1), now)

    accesses = Accesses()
    accesses_data = accesses.get_as_list(now - timedelta(days_back - 1), now)

    erg = []
    for i in range(0, len(uptime_data)):
        if uptime_data[i]['date'] != accesses_data[i]['date']:
            return -1

        erg.append({
            'date': uptime_data[i]['date'],
            'raspberryUptime': uptime_data[i]['raspberryUptime'],
            'apUptime': uptime_data[i]['apUptime'],
            'accesses': accesses_data[i]['accesses']
        })

    return erg
