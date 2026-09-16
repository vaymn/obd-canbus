from dataclasses import dataclass

@dataclass(frozen=True)
class ObdReading:
    pid: int
    name: str
    value: float