#!/usr/bin/python3
import gzip
import os
import re
from datetime import datetime


class ReadLog:
    def __init__(self, directory: str, match_name: str = '.*'):
        if not os.path.exists(directory):
            raise FileNotFoundError
        if not os.path.isdir(directory):
            raise NotADirectoryError
        self._directory = directory
        self._match_name = match_name
        self._log_files = []
        self._logs = []
        self.update_logs()

    @property
    def directory(self):
        return self.directory

    @directory.setter
    def directory(self, value):
        if not os.path.exists(value):
            raise FileNotFoundError
        if not os.path.isdir(value):
            raise NotADirectoryError
        self._directory = value

    @property
    def match_name(self):
        return self._match_name

    @match_name.setter
    def match_name(self, value):
        self._match_name = value

    @property
    def log_files(self):
        return self._log_files.copy()

    @property
    def logs(self):
        return self._logs.copy()

    def __get_log_files(self):
        for element in os.listdir(self._directory):
            element_path = os.path.join(self._directory, element)
            if os.path.isfile(element_path) and re.match(self._match_name, os.path.basename(element_path)):
                self._log_files.append(element_path)

    def __read_logs(self):
        for file in self._log_files:
            if os.path.splitext(file)[-1] == '.gz':
                with gzip.open(file, 'r') as f:
                    for line in f.readlines():
                        self._logs.append(self.__interpret_log(line.decode('utf-8').strip()))
            else:
                with open(file, 'r') as f:
                    for line in f.readlines():
                        self._logs.append(self.__interpret_log(line.strip()))

    def __interpret_log(self, line: str):
        data = re.match(
            '(.*?) (.*?) .*? .*? \\[(.*)] \\"(.*?)\\" (\\d+|-) (\\d+|-) \\"(.*?)\\" \\"(.*)\\"',
            line)
        return {
            "destination": data.group(1),
            "source": data.group(2),
            "timestamp": datetime.strptime(data.group(3), '%d/%b/%Y:%H:%M:%S %z'),
            "request": data.group(4),
            "responsecode": data.group(5),
            "bytes_sent": data.group(6),
            "domain": data.group(7),
            "client_header": data.group(8)
        }

    def update_logs(self):
        self.__get_log_files()
        self.__read_logs()
