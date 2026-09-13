from dataclasses import dataclass
from threading import Lock

@dataclass
class VehicleSnapshot:
    rpm: int

class VehicleState:
    def __init__(self):
        self._lock = Lock()
        self._rpm = 0

    def set_rpm(self, rpm):
        with self._lock:
            self._rpm = rpm

    def snapshot(self):
        with self._lock:
            return VehicleSnapshot(
                rpm=self._rpm
            )