"""Self-contained synthetic vehicle profiles used by the CAN simulator."""

import math


SCENARIOS = {
    "idle": "Moteur au ralenti, véhicule à l'arrêt.",
    "city": "Trafic urbain avec arrêts et accélérations.",
    "highway": "Conduite stabilisée sur autoroute.",
    "overheat": "Conduite avec une température moteur qui monte.",
}


def get_readings(scenario, elapsed):
    """Build decoded dashboard values at a given number of seconds."""
    t = max(0.0, elapsed)
    if scenario == "idle":
        speed = 0
        rpm = 780 + 20 * math.sin(t / 2)
        throttle = 3
        coolant = 88
        intake = 25
        oil = 92
        load = 18
    elif scenario == "highway":
        speed = 112 + 5 * math.sin(t / 18)
        rpm = 2150 + 90 * math.sin(t / 12)
        throttle = 21 + 3 * math.sin(t / 9)
        coolant = 91
        intake = 31
        oil = 98
        load = 34 + 5 * math.sin(t / 10)
    elif scenario == "overheat":
        speed = 58 + 22 * math.sin(t / 10)
        rpm = 1650 + 500 * math.sin(t / 8)
        throttle = 24 + 14 * max(0, math.sin(t / 8))
        coolant = min(128, 102 + t / 12) + 1.5 * math.sin(t / 5)
        intake = 38
        oil = min(145, 112 + t / 15)
        load = 42 + 18 * max(0, math.sin(t / 8))
    else:  # city
        speed = max(0, 42 + 45 * math.sin(t / 13))
        rpm = 850 + speed * 31 + 220 * math.sin(t / 3)
        throttle = 8 + 36 * max(0, math.sin(t / 13))
        coolant = 89
        intake = 29
        oil = 95
        load = 22 + 26 * max(0, math.sin(t / 13))

    speed = max(0, min(200, speed))
    rpm = max(0, min(8000, rpm))
    throttle = max(0, min(100, throttle))
    load = max(0, min(100, load))
    return {
        "speed": speed,
        "rpm": rpm,
        "throttle_position": throttle,
        "engine_load": load,
        "maf": max(0, rpm * load / 500),
        "ignition_timing": 12 + 4 * math.sin(t / 6),
        "coolant_temp": coolant,
        "intake_temp": intake,
        "oil_temp": oil,
        "ambient_temp": 22,
        "fuel_level": 68,
        "control_voltage": 14.1 + 0.15 * math.sin(t / 7),
        "engine_runtime": t,
        "fuel_rate": max(0, rpm * load / 3000),
    }

