from rich import print as rprint
from rich.console import Console
from rich.live import Live
import time
from threading import Event
from vehicle.vehicle_service import VehicleService


class TerminalUi:
    def __init__(self, vehicle_service: VehicleService):
        self._vehicle_service = vehicle_service
        self._console = Console()        

    def display(self, stop_signal: Event):
        with Live(console=self._console, refresh_per_second=10) as live:
            while not stop_signal.is_set():
                snapshot = self._vehicle_service.get_vehicle_snapshot()
                live.update(f"RPM: {snapshot.rpm}")

                stop_signal.wait(0.1)