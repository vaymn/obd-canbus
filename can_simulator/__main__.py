"""Answer Mode 01 OBD-II requests with values from a selected scenario."""

import argparse
import time

from .scenarios import SCENARIOS, get_readings


REQUEST_IDS = {0x7DF, *range(0x7E0, 0x7E8)}
RESPONSE_BASE_ID = 0x7E8


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simulate an OBD-II ECU on a CAN interface."
    )
    parser.add_argument(
        "--scenario",
        choices=sorted(SCENARIOS),
        default="city",
        help="driving scenario to simulate (default: city)",
    )
    parser.add_argument("--interface", default="socketcan")
    parser.add_argument("--channel", default="vcan0")
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="list available scenarios and exit",
    )
    return parser.parse_args()


def encode_pid(pid, readings):
    """Return the raw OBD payload bytes for a supported Mode 01 PID."""
    value = readings
    if pid == 0x04:
        raw = [round(value["engine_load"] * 255 / 100)]
    elif pid in (0x05, 0x0F, 0x46, 0x5C):
        temperature_fields = {
            0x05: "coolant_temp",
            0x0F: "intake_temp",
            0x46: "ambient_temp",
            0x5C: "oil_temp",
        }
        field = temperature_fields[pid]
        raw = [round(value[field] + 40)]
    elif pid == 0x0C:
        rpm = round(value["rpm"] * 4)
        raw = [(rpm >> 8) & 0xFF, rpm & 0xFF]
    elif pid == 0x0D:
        raw = [round(value["speed"])]
    elif pid == 0x0E:
        raw = [round((value["ignition_timing"] + 64) * 2)]
    elif pid == 0x10:
        maf = round(value["maf"] * 100)
        raw = [(maf >> 8) & 0xFF, maf & 0xFF]
    elif pid == 0x11:
        raw = [round(value["throttle_position"] * 255 / 100)]
    elif pid == 0x1F:
        runtime = min(65535, round(value["engine_runtime"]))
        raw = [(runtime >> 8) & 0xFF, runtime & 0xFF]
    elif pid == 0x2F:
        raw = [round(value["fuel_level"] * 255 / 100)]
    elif pid == 0x42:
        voltage = round(value["control_voltage"] * 1000)
        raw = [(voltage >> 8) & 0xFF, voltage & 0xFF]
    elif pid == 0x5E:
        rate = round(value["fuel_rate"] * 20)
        raw = [(rate >> 8) & 0xFF, rate & 0xFF]
    else:
        return None

    return bytes(max(0, min(255, byte)) for byte in raw)


def response_for(request, pid, payload):
    import can

    response_id = (
        RESPONSE_BASE_ID + request.arbitration_id - 0x7E0
        if 0x7E0 <= request.arbitration_id <= 0x7E7
        else RESPONSE_BASE_ID
    )
    data = bytes([len(payload) + 2, 0x41, pid]) + payload
    data = data.ljust(8, b"\x00")
    return can.Message(
        arbitration_id=response_id,
        data=data,
        is_extended_id=False,
    )


def main():
    args = parse_args()
    if args.list_scenarios:
        for name, description in SCENARIOS.items():
            print(f"{name:10} {description}")
        return

    import can

    print(
        f"Scénario « {args.scenario} » sur {args.interface}:{args.channel}. "
        "Ctrl+C pour arrêter."
    )
    started = time.monotonic()
    bus = can.Bus(interface=args.interface, channel=args.channel)
    try:
        while True:
            request = bus.recv(timeout=0.5)
            if request is None or request.is_extended_id or request.is_remote_frame:
                continue
            if request.arbitration_id not in REQUEST_IDS or len(request.data) < 3:
                continue
            if request.data[1] != 0x01:
                continue

            pid = request.data[2]
            readings = get_readings(args.scenario, time.monotonic() - started)
            payload = encode_pid(pid, readings)
            if payload is not None:
                bus.send(response_for(request, pid, payload))
    except KeyboardInterrupt:
        print("\nSimulateur arrêté.")
    finally:
        bus.shutdown()


if __name__ == "__main__":
    main()

