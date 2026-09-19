from dataclasses import dataclass
from obd.obd_reading import ObdReading
from vehicle.vehicle_state import VehicleState

class VehicleService:
    def __init__(self):
        self._vehicle_state = VehicleState()

    def get_vehicle_snapshot(self):
        return self._vehicle_state.snapshot()

    def set_vehicle_rpm(self, rpm):
        self._vehicle_state.set_rpm(rpm)

    def update_reading(self, reading: ObdReading):
        self._vehicle_state.update(reading.name, reading.value)
