import can
import signal
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
        self._threads = []

    def stop(self, signum=None, frame=None):
        """Request a clean shutdown of all application threads."""
        if not self._stop.is_set():
            print("\nArrêt de l'application...")
            self._stop.set()

    def run(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        self._threads = [
            Thread(
                target=self._receiver.run,
                args=(self._stop,),
                name="can_receiver"
            ),
            Thread(
                target=self._requestor.run,
                args=(self._stop,),
                name="can_requestor"
            ),
            Thread(
                target=self._ui.display,
                args=(self._stop,),
                name="ui_thread"
            ),
        ]

        try:
            for thread in self._threads:
                thread.start()

            # Attend un signal d'arrêt sans bloquer indéfiniment.
            while not self._stop.wait(0.5):
                pass

        finally:
            # Garantit que tous les composants reçoivent le signal, même si
            # une exception survient dans le thread principal.
            self._stop.set()

            for thread in self._threads:
                thread.join(timeout=2.0)

            self._bus.shutdown()
            print("Application arrêtée.")

if __name__ == "__main__":
    Application().run()
