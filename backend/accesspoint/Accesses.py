#!/usr/bin/python3
from datetime import datetime, timedelta
from random import randrange


class Accesses:
    def __init__(self):
        self._accesses = []
        self.__get_accesses()

    @property
    def accesses(self):
        return self._accesses.copy()

    def __get_accesses(self, ):
        pass

    def get_as_list(self, start: datetime.date = None, end: datetime.date = datetime.now().date()):
        if not start:
            start = min(self._accesses)

        erg = []
        current = start
        while current <= end:
            erg.append({
                'date': str(current),
                'accesses': randrange(10, 40),
            })
            current += timedelta(days=1)

        return erg
