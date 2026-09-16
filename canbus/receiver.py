import can
from obd import obd
from threading import Event
from vehicle.vehicle_service import VehicleService

class CanReceiver:

    def __init__(self, bus, vehicle_service: VehicleService):
        self._bus = bus
        self._vehicle_service = vehicle_service

    def run(self, stop_signal: Event):
        while not stop_signal.is_set():
            try: 
                msg = self._bus.recv(timeout=1.0)

                if msg is None:
                    continue

                reading = obd.parse_obd_response(msg)

                if reading is not None and reading.name == 'rpm':
                    self._vehicle_service.set_vehicle_rpm(reading.value)

            except can.CanError as e:
                print(f"CAN error: {e}")
            
            stop_signal.wait(0.1) #10Hz