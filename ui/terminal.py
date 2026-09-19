from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
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
                live.update(render_dashboard(snapshot))

                stop_signal.wait(0.1)


def render_dashboard(snapshot):
    table = Table(title="Combiné d'instruments", expand=True)
    table.add_column("Information", style="cyan", no_wrap=True)
    table.add_column("Valeur", style="white")

    table.add_row("Vitesse", gauge(snapshot.speed, 200, 40, "km/h", 5))
    table.add_row("Régime moteur", gauge(snapshot.rpm, 10000, 40, "tr/min", 250))
    table.add_section()

    table.add_row("Température liquide refroidissement", format_value(snapshot.coolant_temp, 1, "°C"))
    table.add_row("Température air admission", format_value(snapshot.intake_temp, 1, "°C"))
    table.add_row("Température huile", format_value(snapshot.oil_temp, 1, "°C"))
    table.add_row("Température extérieure", format_value(snapshot.ambient_temp, 1, "°C"))
    table.add_row("Charge moteur", format_value(snapshot.engine_load, 1, "%"))
    table.add_row("Position accélérateur", format_value(snapshot.throttle_position, 1, "%"))
    table.add_row("Niveau carburant", format_value(snapshot.fuel_level, 1, "%"))
    table.add_row("Tension calculateur", format_value(snapshot.control_voltage, 2, "V"))
    table.add_row("Débit d'air MAF", format_value(snapshot.maf, 2, "g/s"))
    table.add_row("Avance allumage", format_value(snapshot.ignition_timing, 1, "°"))
    table.add_row("Temps moteur", format_duration(snapshot.engine_runtime))
    table.add_row("Débit carburant", format_value(snapshot.fuel_rate, 2, "L/h"))

    return table


def gauge(value, maximum, width, unit, step):
    if value is None:
        return Text(f"{'░' * width}  -- {unit}", style="dim")

    bounded_value = max(0, min(float(value), maximum))
    filled = round(bounded_value / maximum * width)
    bar = "█" * filled + "░" * (width - filled)
    scale = f"0 ├{'─' * (width - 2)}┤ {maximum:g}"

    result = Text()
    result.append(f"{bar}  ", style="green")
    result.append(f"{bounded_value:.0f} {unit}")
    return result


def format_value(value, decimals, unit):
    if value is None:
        return "--"
    return f"{value:.{decimals}f} {unit}"


def format_duration(seconds):
    if seconds is None:
        return "--"

    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
