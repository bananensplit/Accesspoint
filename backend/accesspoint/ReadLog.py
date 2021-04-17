#!/usr/bin/python3
import gzip
import os
import re
import threading
from datetime import datetime


class ReadLog:
    def __init__(self, directory: str, match_file: str = '.*', match_line: str = '.*'):
        if not os.path.exists(directory):
            raise FileNotFoundError
        if not os.path.isdir(directory):
            raise NotADirectoryError
        self._directory = directory
        self._match_file = match_file
        self._match_line = match_line
        self._log_files = []
        self._logs = []
        self.__get_log_files()
        self.__read_logs()

    @property
    def directory(self):
        return self.directory

    @property
    def match_name(self):
        return self._match_file

    @property
    def match_line(self):
        return self._match_line

    @property
    def log_files(self):
        return self._log_files.copy()

    @property
    def logs(self):
        return self._logs.copy()

    def __get_log_files(self):
        for element in os.listdir(self._directory):
            element_path = os.path.join(self._directory, element)
            if os.path.isfile(element_path) and re.match(self._match_file, os.path.basename(element_path)):
                self._log_files.append(element_path)

    def __read_logs(self):
        threads = []
        for file in self._log_files:
            thread = threading.Thread(target=self.__read_log_file, args=(file,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    def __read_log_file(self, file):
        if os.path.splitext(file)[-1] == '.gz':
            with gzip.open(file, 'r') as f:
                for line in f.readlines():
                    line = line.decode('utf-8').strip()
                    if re.match(self._match_line, line):
                        self._logs.append(line)
        else:
            with open(file, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if re.match(self._match_line, line):
                        self._logs.append(line)

    @staticmethod
    def interpret_log(line: str):
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
        self._log_files = []
        self._logs = []
        self.__get_log_files()
        self.__read_logs()
