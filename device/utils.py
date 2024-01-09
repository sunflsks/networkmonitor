import threading
import time
from cellular import PingResult
import random
from gps import GPSPosition

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
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False

def generate_random_ping():
  return PingResult(
    hostname="example.com",
    ip_address="0.0.0.0",
    latency=random.uniform(0, 100),
    packet_dropped=0,
    rssi=random.randint(-100, 0),
    gpsinfo=GPSPosition(success=False, latitude=-100, longitude=100)
  )