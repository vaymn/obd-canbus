import can
from dataclasses import dataclass
from typing import Optional
from .obd_reading import ObdReading

@dataclass
class ObdResponse:
    ecu_id: int
    mode: int
    pid: int
    payload: bytes

def parse_obd_response(msg: can.Message) -> Optional[ObdReading]:
    if not (0x7E8 <= msg.arbitration_id <= 0x7EF):
        return None

    data = msg.data

    if len(data) < 3:
        return None

    length = data[0]
    mode = data[1]

    # Response to Mode 01 = 0x41
    if mode != 0x41:
        return None

    pid = data[2]

    payload_length = max(0, length - 2)
    payload = bytes(data[3:3 + payload_length])

    obd_response = ObdResponse(
        ecu_id=msg.arbitration_id,
        mode=mode,
        pid=pid,
        payload=payload
    )

    return decode_pid(obd_response.pid, obd_response.payload)

def decode_pid(pid: int, data: bytes):
    match pid:
        case 0x04:  # Calculated engine load
            return _one_byte(pid, data, "engine_load", lambda value: value * 100 / 255)
        case 0x05:  # Coolant temperature
            return _one_byte(pid, data, "coolant_temp", lambda value: value - 40)
        case 0x0C:  # Engine RPM
            return _two_bytes(pid, data, "rpm", lambda value: value / 4)
        case 0x0D:  # Vehicle speed
            return _one_byte(pid, data, "speed", float)
        case 0x0E:  # Ignition timing advance
            return _one_byte(pid, data, "ignition_timing", lambda value: value / 2 - 64)
        case 0x0F:  # Intake air temperature
            return _one_byte(pid, data, "intake_temp", lambda value: value - 40)
        case 0x10:  # Mass air flow
            return _two_bytes(pid, data, "maf", lambda value: value / 100)
        case 0x11:  # Throttle position
            return _one_byte(pid, data, "throttle_position", lambda value: value * 100 / 255)
        case 0x1F:  # Engine run time
            return _two_bytes(pid, data, "engine_runtime", float)
        case 0x2F:  # Fuel tank level
            return _one_byte(pid, data, "fuel_level", lambda value: value * 100 / 255)
        case 0x42:  # Control module voltage
            return _two_bytes(pid, data, "control_voltage", lambda value: value / 1000)
        case 0x46:  # Ambient air temperature
            return _one_byte(pid, data, "ambient_temp", lambda value: value - 40)
        case 0x5C:  # Engine oil temperature
            return _one_byte(pid, data, "oil_temp", lambda value: value - 40)
        case 0x5E:  # Engine fuel rate
            return _two_bytes(pid, data, "fuel_rate", lambda value: value / 20)

    return None


def _one_byte(pid: int, data: bytes, name: str, decoder) -> Optional[ObdReading]:
    if len(data) < 1:
        return None
    return ObdReading(pid, name, decoder(data[0]))


def _two_bytes(pid: int, data: bytes, name: str, decoder) -> Optional[ObdReading]:
    if len(data) < 2:
        return None
    raw_value = (data[0] << 8) | data[1]
    return ObdReading(pid, name, decoder(raw_value))
