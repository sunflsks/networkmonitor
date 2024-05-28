import threading
import time
import random
from constants import LEDCTL
import re
import subprocess


class LockableObject:
    def __init__(self, value):
        self._lock = threading.Lock()
        self.value = value

    def __enter__(self):
        self._lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()


# Credit to https://stackoverflow.com/a/40965385/13820469
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.daemon = True
            self._timer.start()
            self.is_running = True

    def stop(self):
        if self._timer:
            self._timer.cancel()
            self.is_running = False

def get_modem_path() -> str:
    # Example output: /org/freedesktop/ModemManager1/Modem/0 [QUALCOMM INCORPORATED] SIMCOM_SIM7600G-H
    output = subprocess.check_output(["mmcli", "-L"]).decode("utf-8")
    match = re.search(r"/org/freedesktop/ModemManager1/Modem/\d+", output)
    if match:
        return match.group(0)
    return ""
