from dataclasses import dataclass


@dataclass(frozen=True)
class PidDefinition:
    pid: int
    name: str
    interval: float


# Fréquences adaptées à un combiné d'instruments : les valeurs dynamiques
# sont interrogées plus souvent que les températures et les niveaux.
PID_DEFINITIONS = (
    PidDefinition(0x0C, "rpm", 0.10),
    PidDefinition(0x0D, "speed", 0.10),
    PidDefinition(0x11, "throttle_position", 0.20),
    PidDefinition(0x04, "engine_load", 0.50),
    PidDefinition(0x10, "maf", 0.50),
    PidDefinition(0x0E, "ignition_timing", 0.50),
    PidDefinition(0x05, "coolant_temp", 1.00),
    PidDefinition(0x0F, "intake_temp", 1.00),
    PidDefinition(0x42, "control_voltage", 1.00),
    PidDefinition(0x5C, "oil_temp", 1.00),
    PidDefinition(0x2F, "fuel_level", 2.00),
    PidDefinition(0x46, "ambient_temp", 2.00),
    PidDefinition(0x1F, "engine_runtime", 2.00),
    PidDefinition(0x5E, "fuel_rate", 1.00),
)

PIDS = {definition.name: definition.pid for definition in PID_DEFINITIONS}
