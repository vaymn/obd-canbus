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
            case 0x0C: #RPM
                if len(data) < 2:
                    return None

                a, b = data[0], data[1]
                rpm = ((a << 8) | b) / 4
                return ObdReading(pid, 'rpm', rpm)

            case 0x0D: #Speed
                if len(data) < 1:
                    return None
                return ObdReading(pid, 'speed', data[0])

            case 0x05: #Coolant temp
                if len(data) < 1:
                    return None
                
                coolant_temp = data[0] - 40
                return ObdReading(pid, 'coolant_temp', coolant_temp)

            case 0x11: #Throttle position:
                if len(data) < 1:
                    return None
                
                throttle_position = data[0] * 100 / 255
                return ObdReading(pid, 'throttle_position', throttle_position)
