import can
import argparse
import signal
from threading import Event, Thread
from canbus import receiver, requestor
from vehicle.vehicle_service import VehicleService
from ui.terminal import TerminalUi

DEFAULT_INTERFACE = "socketcan"
DEFAULT_CHANNEL = "vcan0"

class Application:
    def __init__(self, interface=DEFAULT_INTERFACE, channel=DEFAULT_CHANNEL):
        self._bus = can.Bus(
            channel=channel,
            interface=interface
        )

        self._vehicle_service = VehicleService()
        self._stop = Event()

        self._receiver = receiver.CanReceiver(
            self._bus,
            self._vehicle_service
        )
        self._requestor = requestor.CanRequestor(self._bus)

        self._ui = TerminalUi(self._vehicle_service)

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

def parse_args():
    parser = argparse.ArgumentParser(
        description="Interroge un véhicule via CAN/OBD-II."
    )
    parser.add_argument(
        "--interface",
        default=DEFAULT_INTERFACE,
        help=f"Interface python-can à utiliser (défaut : {DEFAULT_INTERFACE})"
    )
    parser.add_argument(
        "--channel",
        default=DEFAULT_CHANNEL,
        help=f"Canal CAN à utiliser (défaut : {DEFAULT_CHANNEL})"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    Application(
        interface=args.interface,
        channel=args.channel
    ).run()
