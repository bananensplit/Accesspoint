#!/usr/bin/python3
import re
from datetime import datetime, timedelta

from accesspoint.ReadLog import ReadLog


class Accesses:
    def __init__(self, readlog: ReadLog, match_destination: str, match_reqeust: str = 'GET / HTTP.*'):
        self._daily_accesses = {}
        self._readlog = readlog
        self._match_destination = match_destination
        self._match_request = match_reqeust
        self.update_accesses()

    @property
    def daily_accesses(self):
        return self._daily_accesses.copy()

    @property
    def match_destination(self):
        return self._match_destination

    @property
    def match_request(self):
        return self._match_request

    def __get_daily_accesses(self, ):
        for log in self._readlog.logs:
            print(log)
            if re.match(self._match_request, log['request']) and re.match(self._match_destination, log['destination']):
                if log['timestamp'].date() in self._daily_accesses:
                    self._daily_accesses[log['timestamp'].date()].append(log)
                else:
                    self._daily_accesses[log['timestamp'].date()] = [log]

    def get_number_accesses(self, start: datetime.date = None, end: datetime.date = datetime.now().date()):
        if not start:
            start = min(self._daily_accesses)

        erg = []
        current = start
        while current <= end:
            erg.append({
                'date': str(current),
                'accesses': len(self._daily_accesses[current]) if current in self._daily_accesses else 0,
            })
            current += timedelta(days=1)

        return erg

    def update_accesses(self):
        self.__get_daily_accesses()


if __name__ == '__main__':
    accesses = Accesses(ReadLog('../Resources', 'other_vhosts_access\\.log.*'), '.*:2000')
    for x in accesses.get_number_accesses():
        print(x)