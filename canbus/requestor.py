import can
import time
from threading import Event

PIDS = {
    "rpm": 0x0C,
    "speed": 0x0D,
    "coolant": 0x05,
    "throttle": 0x11,
    "voltage": 0x42,
}

class CanRequestor:

    def __init__(self, bus):
        self._bus = bus

    def request_pid(pid):
        data = bytes([
            0x02, # length
            0x01, # mode 01
            pid,
            0, 0, 0, 0, 0
        ])

        message = can.Message(
            arbitration_id=0x7DF,
            data=data,
            is_extended_id=False
        )

        self._bus.send(message)

    def run(self, stop_signal: Event):
        while not stop_signal.is_set():
            for name, pid in PIDS.items():
                request_pid(pid)
            stop_signal.wait(0.1)