import can
import time
from threading import Event
from obd.pids import PID_DEFINITIONS

class CanRequestor:

    def __init__(self, bus):
        self._bus = bus

    def request_pid(self, pid):
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
        next_request = {definition.pid: 0.0 for definition in PID_DEFINITIONS}

        while not stop_signal.is_set():
            now = time.monotonic()

            for definition in PID_DEFINITIONS:
                if now >= next_request[definition.pid]:
                    try:
                        self.request_pid(definition.pid)
                    except can.CanError as error:
                        print(f"CAN error lors de l'envoi du PID 0x{definition.pid:02X}: {error}")
                    next_request[definition.pid] = now + definition.interval

            next_due = min(next_request.values())
            stop_signal.wait(max(0.01, min(0.10, next_due - time.monotonic())))
