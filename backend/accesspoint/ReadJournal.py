#!/usr/bin/python3
import json
import re
import subprocess
from datetime import datetime


class ReadJournal:
    def __init__(self):
        self._journal = []
        self._clean_journal = []
        self._boots = []
        self.update_journals()

    @property
    def journal(self):
        return self._journal.copy()

    @property
    def clean_journal(self):
        return self._clean_journal.copy()

    @property
    def boots(self):
        return self._boots.copy()

    def __read_journal(self):
        command = 'journalctl -u hostapd.service -o json --no-pager JOB_TYPE=start JOB_TYPE=stop JOB_RESULT=done --output-fields=JOB_TYPE,_SOURCE_REALTIME_TIMESTAMP'
        process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self._journal = [json.loads(x) for x in process.stdout.read().decode('UTF-8').split('\n')[:-1]]

    def __interpret_journal(self):
        self._clean_journal = [{
            'time': datetime.fromtimestamp(int(x['_SOURCE_REALTIME_TIMESTAMP']) / 1000000),
            'job_type': x['JOB_TYPE'] == 'start'
        } for x in self._journal]

    def __read_boots(self):
        command = 'journalctl --list-boots'
        process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        data = process.stdout.read().decode('UTF-8').split('\n')[:-1]

        def interpret_boot(line: str):
            regex = re.match(
                r'.*? (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?—.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?',
                line.strip())
            return {
                "start_time": datetime.strptime(regex.group(1), "%Y-%m-%d %X"),
                "stop_time": datetime.strptime(regex.group(2), "%Y-%m-%d %X")
            }

        self._boots = [interpret_boot(x) for x in data]

    def update_journals(self):
        self.__read_journal()
        self.__interpret_journal()
        self.__read_boots()
