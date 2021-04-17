#!/usr/bin/python3
import copy
from datetime import timedelta, datetime, date, timezone

from accesspoint.ReadJournal import ReadJournal


class Uptime:
    def __init__(self, journal: ReadJournal = ReadJournal()):
        self._journal = journal
        self._rp_uptimes = {}
        self._ap_uptimes = {}
        self.__get_rp_uptimes()
        self.__get_ap_uptimes()

    @property
    def ap_uptimes(self):
        return copy.deepcopy(self._ap_uptimes)

    @property
    def rp_uptimes(self):
        return copy.deepcopy(self._rp_uptimes)

    @staticmethod
    def __format_data(data):
        erg = {}

        def sort_and_insert_by_day():
            beginning = min(data, key=lambda el: el['time'])['time'].date()
            ending = date.today()
            for i in range(0, (ending - beginning).days + 1):
                erg[beginning + timedelta(i)] = []

            for i in data:
                if erg[i['time'].date()] and not erg[i['time'].date()][-1]['job_type'] and not i['job_type']:
                    continue
                erg[i['time'].date()].append(i)

        def insert_per_day_actions():
            current_state = False
            for i in erg:
                element = erg[i]
                current_day_datetime = datetime(i.year, i.month, i.day)

                if not element:
                    if current_state:
                        element.append({
                            'time': current_day_datetime.replace(hour=0, minute=0, second=0, microsecond=0),
                            'job_type': True
                        })

                        if current_day_datetime.date() == date.today():
                            element.append({
                                'time': datetime.now(),
                                'job_type': False
                            })
                        else:
                            element.append({
                                'time': current_day_datetime.replace(hour=23, minute=59, second=59, microsecond=999999),
                                'job_type': False
                            })
                    continue

                current_state = element[-1]['job_type']
                if not element[0]['job_type']:
                    element.insert(0, {
                        'time': current_day_datetime.replace(hour=0, minute=0, second=0, microsecond=0),
                        'job_type': True
                    })

                if element[-1]['job_type']:
                    if i == date.today():
                        element.append({
                            'time': datetime.now(),
                            'job_type': False
                        })
                    else:
                        element.append({
                            'time': current_day_datetime.replace(hour=23, minute=59, second=59, microsecond=999999),
                            'job_type': False
                        })

        def convert_to_seconds():
            for i in erg:
                for j in erg[i]:
                    j['time'] = j['time'].replace(year=1970, month=1, day=1, tzinfo=timezone.utc).timestamp()

        sort_and_insert_by_day()
        insert_per_day_actions()
        convert_to_seconds()
        return erg

    def __get_ap_uptimes(self):
        self._ap_uptimes = self.__format_data(self._journal.clean_journal)

    def __get_rp_uptimes(self):
        erg = []
        for element in self._journal.boots:
            erg.append({'time': element['start_time'], 'job_type': True})
            erg.append({'time': element['stop_time'], 'job_type': False})
        erg.append({'time': datetime.now(), 'job_type': False})

        self._rp_uptimes = self.__format_data(erg)

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
                'rp-actions': self._rp_uptimes[current] if current in self._rp_uptimes else [],
                'ap-actions': self._ap_uptimes[current] if current in self._ap_uptimes else []
            })
            current += timedelta(days=1)

        return erg

    def update_uptimes(self):
        self._journal.update_journals()
        self._rp_uptimes = {}
        self._ap_uptimes = {}
        self.__get_rp_uptimes()
        self.__get_ap_uptimes()
