#!/usr/bin/python3
from datetime import timedelta, datetime

from accesspoint.ReadJournal import ReadJournal


class Uptime:
    def __init__(self, journal: ReadJournal = ReadJournal()):
        self._journal = journal
        self._ap_uptimes = {}
        self._rp_uptimes = {}
        self.__get_ap_uptimes()
        self.__get_rp_uptimes()

    @property
    def ap_uptimes(self):
        return self._ap_uptimes.copy()

    @property
    def rp_uptimes(self):
        return self._rp_uptimes.copy()

    def __get_ap_uptimes(self):
        erg = self._journal.clean_journal
        erg.append({'time': datetime.now(), 'job_type': False})
        uptimes = {}

        def insert_shutdowns():
            counter = 0
            for i, element in enumerate(erg):
                if i >= len(erg) - 1 or counter >= len(self._journal.boots):
                    break

                if element['time'] < self._journal.boots[counter]['stop_time'] < erg[i + 1]['time']:
                    erg.insert(i + 1, {
                        'time': self._journal.boots[counter]['stop_time'],
                        'job_type': False
                    })
                    counter += 1

        def insert_per_day_actions():
            skip_next = False
            for i, element in enumerate(erg):
                if i >= len(erg) - 1:
                    break

                if skip_next:
                    skip_next = False
                    continue

                if element['time'].date() != erg[i + 1]['time'].date():
                    erg.insert(i + 1, {
                        'time': element['time'].replace(hour=23, minute=59, second=59, microsecond=999999),
                        'job_type': not element['job_type']
                    })
                    erg.insert(i + 2, {
                        'time': element['time'].replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
                        'job_type': element['job_type']
                    })
                    skip_next = True

        def sort_by_day():
            for x in erg:
                if x['time'].date() in uptimes.keys():
                    uptimes[x['time'].date()].append(x)
                else:
                    uptimes[x['time'].date()] = [x]

        def calculate_seconds():
            for key, day in uptimes.items():
                uptime = 0
                for i, element in enumerate(day[:-1]):
                    if not element['job_type']:
                        continue
                    else:
                        uptime += (day[i + 1]['time'] - element['time']).total_seconds()
                uptimes[key] = uptime

        insert_shutdowns()
        insert_per_day_actions()
        sort_by_day()
        calculate_seconds()
        self._ap_uptimes = uptimes

    def __get_rp_uptimes(self):
        uptimes = {}

        erg = []
        for element in self._journal.boots:
            erg.append({'time': element['start_time'], 'job_type': True})
            erg.append({'time': element['stop_time'], 'job_type': False})
        erg.append({'time': datetime.now(), 'job_type': False})

        def insert_per_day_actions():
            skip_next = False
            for i, element in enumerate(erg):
                if i >= len(erg) - 1:
                    break

                if skip_next:
                    skip_next = False
                    continue

                if element['time'].date() != erg[i + 1]['time'].date():
                    erg.insert(i + 1, {
                        'time': element['time'].replace(hour=23, minute=59, second=59, microsecond=999999),
                        'job_type': not element['job_type']
                    })
                    erg.insert(i + 2, {
                        'time': element['time'].replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
                        'job_type': element['job_type']
                    })
                    skip_next = True

        def sort_by_day():
            for x in erg:
                if x['time'].date() in uptimes.keys():
                    uptimes[x['time'].date()].append(x)
                else:
                    uptimes[x['time'].date()] = [x]

        def calculate_seconds():
            for key, day in uptimes.items():
                uptime = 0
                for i, element in enumerate(day[:-1]):
                    if not element['job_type']:
                        continue
                    else:
                        uptime += (day[i + 1]['time'] - element['time']).total_seconds()
                uptimes[key] = uptime

        insert_per_day_actions()
        sort_by_day()
        calculate_seconds()
        self._rp_uptimes = uptimes

    def __str__(self):
        erg = "AP-Uptimes:\n"
        for key, seconds in self._ap_uptimes.items():
            erg += f'{key}: {int(seconds / 60 // 60) * "|"} {seconds}s\n'

        erg += "\nRP-Uptimes:\n"
        for key, seconds in self._rp_uptimes.items():
            erg += f'{key}: {int(seconds / 60 // 60) * "|"} {seconds}s\n'
        return erg

    def get_as_list(self, start: datetime.date = None, end: datetime.date = datetime.now().date()):
        if not start:
            start = min(min(self._ap_uptimes), min(self._rp_uptimes))

        erg = []
        current = start
        while current <= end:
            erg.append({
                'date': str(current),
                'raspberryUptime': self._rp_uptimes[current] if current in self._rp_uptimes else 0,
                'apUptime': self._ap_uptimes[current] if current in self._ap_uptimes else 0
            })
            current += timedelta(days=1)

        return erg
