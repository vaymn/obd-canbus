from dataclasses import dataclass
from threading import Lock
from typing import Optional

@dataclass
class VehicleSnapshot:
    rpm: Optional[float] = None
    speed: Optional[float] = None
    coolant_temp: Optional[float] = None
    throttle_position: Optional[float] = None
    engine_load: Optional[float] = None
    intake_temp: Optional[float] = None
    fuel_level: Optional[float] = None
    control_voltage: Optional[float] = None
    ambient_temp: Optional[float] = None
    oil_temp: Optional[float] = None
    maf: Optional[float] = None
    ignition_timing: Optional[float] = None
    engine_runtime: Optional[float] = None
    fuel_rate: Optional[float] = None

class VehicleState:
    def __init__(self):
        self._lock = Lock()
        self._values = {}

    def set_rpm(self, rpm):
        self.update("rpm", rpm)

    def update(self, name, value):
        with self._lock:
            if hasattr(VehicleSnapshot, name):
                self._values[name] = value

    def snapshot(self):
        with self._lock:
            return VehicleSnapshot(**self._values)
