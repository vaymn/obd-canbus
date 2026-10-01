# CAN OBD-II Scenario Simulator

This directory is a standalone simulator. It answers standard OBD-II Mode 01
requests with synthetic CAN frames, so the dashboard can be exercised without
connecting to a vehicle. It does not import code from the rest of the project.

## Requirements

- Python 3.10 or newer
- `python-can` (`python3 -m pip install python-can`)
- Linux SocketCAN for the default `socketcan` interface

## Start a virtual CAN channel

Create the channel once (Linux):

```sh
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
```

From the repository root, run the simulator and the dashboard in separate
terminals:

```sh
python3 -m can_simulator --scenario city
python3 app.py --interface socketcan --channel vcan0
```

The simulator defaults to `city` on `vcan0`. Stop it with Ctrl+C. Use
`--interface` and `--channel` to select another python-can backend or channel.

## Scenarios

List the available profiles with `python3 -m can_simulator --list-scenarios`:

- `idle` — engine running while stopped
- `city` — changing speed and engine load with traffic-like stops
- `highway` — steady high speed and engine load
- `overheat` — coolant and oil temperatures rise over time

The simulator responds to supported Mode 01 PID requests on functional request
ID `0x7DF` or physical IDs `0x7E0`–`0x7E7`, using ECU response IDs `0x7E8`–`0x7EF`.
