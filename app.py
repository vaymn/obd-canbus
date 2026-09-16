import can
from threading import Event, Thread
from canbus import receiver, requestor
from vehicle.vehicle_service import VehicleService
from ui.terminal import TerminalUi

interface = "socketcan"
channel = "vcan0"

class Application:
    def __init__(self):
        self._bus = can.Bus(
            channel=channel,
            interface=interface
        )

        self._vehicle_service = VehicleService()

        self._receiver = receiver.CanReceiver(
            self._bus,
            self._vehicle_service
        )
        self._requestor = requestor.CanRequestor(self._bus)

        self._ui = TerminalUi(self._vehicle_service)

        self._stop = Event()

    def run(self):
        receiver_thread = Thread(
            target=self._receiver.run,
            args=(self._stop,),
            name="can_receiver"
        )

        requestor_thread = Thread(
            target=self._requestor.run,
            args=(self._stop,),
            name="can_requestor"
        )

        ui_thread = Thread(
            target=self._ui.display,
            args=(self._stop,),
            name="ui_thread"
        )

        receiver_thread.start()
        requestor_thread.start()
        ui_thread.start()

if __name__ == "__main__":
    Application().run()

