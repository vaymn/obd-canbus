from dataclasses import dataclass
from vehicle.vehicle_state import VehicleState

class VehicleService:
    def __init__(self):
        self._vehicle_state = VehicleState()

    def get_vehicle_snapshot(self):
        return self._vehicle_state.snapshot()

    def set_vehicle_rpm(self, rpm):
        self._vehicle_state.set_rpm(rpm)