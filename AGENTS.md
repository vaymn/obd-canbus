# Repository Guidelines

## Project Structure & Module Organization

`app.py` is the command-line entry point. The application is divided by responsibility: `canbus/` sends and receives CAN frames, `obd/` defines OBD requests and decodes readings, `vehicle/` maintains vehicle state, and `ui/` renders the terminal dashboard. `commands.md` contains CAN setup and replay commands; `docs.md` records protocol notes. There is currently no dedicated test or asset directory.

## Build, Test, and Development Commands

This repository has no build configuration, dependency manifest, or automated test suite. Install the Python packages used by the code (`python-can` and `rich`) in your environment, then run:

- `python app.py` — start with the default `socketcan` interface and `vcan0` channel.
- `python app.py --interface socketcan --channel can0` — connect to a different SocketCAN channel.

For local development without a vehicle, create and bring up a virtual CAN interface using the VCAN commands in `docs.md`; simulated dashboard traffic can be replayed with the `canplayer` command there.

## Coding Style & Naming Conventions

Use Python with four spaces for indentation. Follow the existing naming patterns: `PascalCase` for classes, `snake_case` for functions, methods, and variables, and uppercase names for module constants. Keep CAN transport, OBD interpretation, vehicle state, and presentation logic in their respective modules. No formatter or linter is configured.

## Testing Guidelines

No tests or test framework are present. When changing protocol decoding or state updates, include representative frame or reading examples in the change description and verify them against the OBD/CAN behavior. Keep any future automated tests in a `tests/` directory and name them `test_*.py`.

## Commit & Pull Request Guidelines

Recent commits use short, direct summaries, often in English or French; no strict prefix convention is established. Keep commit subjects concise and action-oriented. Pull requests should explain the behavior change, list relevant interface or channel settings, and include terminal output or screenshots when changing dashboard presentation. Link related issues when available.

## Hardware and Configuration

The default channel is `vcan0`, which is suitable for simulation. Physical CAN access depends on Linux SocketCAN setup and device permissions; follow `docs.md` and avoid committing machine-specific interface settings or captured vehicle data without removing sensitive information.
