"""Main entry."""

import argparse
import asyncio
import logging
import sys
from enum import IntEnum
from typing import Union

try:
    from . import SpaClient, SpaConnectionError, SpaControl, __version__
    from .enums import SpaState
except ImportError:
    from pybalboa import SpaClient, SpaConnectionError, SpaControl, __version__
    from pybalboa.enums import SpaState


async def run_discovery(first_spa: bool = True) -> None:
    """Attempt to discover a spa and try some commands."""
    spas = await SpaClient.discover(first_spa)
    for spa in spas:
        await connect_and_listen(spa=spa)


async def connect_and_listen(
    host: Union[str, None] = None, spa: Union[SpaClient, None] = None
) -> None:
    """Connect to the spa and try some commands."""
    print("******** Testing spa connection and configuration **********")
    try:
        if host:
            spa = SpaClient(host)
        if not spa:
            print("No spa provided")
            return
        async with spa:
            if not await spa.async_configuration_loaded():
                if spa.state == SpaState.TEST_MODE:
                    print("Config not loaded, spa is in test mode!")
                else:
                    print("Config not loaded, something is wrong!")
                return

            print()
            print("Module identification")
            print("---------------------")
            print(f"MAC address: {spa.mac_address}")
            print(f"iDigi Device Id: {spa.idigi_device_id}")
            print()

            print("Device configuration")
            print("--------------------")
            print(spa.circulation_pump)
            print(f"Pumps: {[pump.name for pump in spa.pumps]}")
            print(f"Lights: {[light.name for light in spa.lights]}")
            print(f"Aux: {[aux.name for aux in spa.aux]}")
            print(f"Blower: {[blower.name for blower in spa.blowers]}")
            print(f"Mister: {[mister.name for mister in spa.misters]}")
            print()

            print("System information")
            print("------------------")
            print(f"Model: {spa.model}")
            print(f"Software version: {spa.software_version}")
            print(f"Configuration signature: {spa.configuration_signature}")
            print(f"Current setup: {spa.current_setup}")
            print(f"Voltage: {spa.voltage}")
            print(f"Heater type: {spa.heater_type}")
            print(f"DIP switch: {spa.dip_switch}")
            print()

            print("Setup parameters")
            print("----------------")
            print(f"Min temps: {spa._low_range}")  # pylint: disable=protected-access
            print(f"Max temps: {spa._high_range}")  # pylint: disable=protected-access
            print(f"Pump count: {spa.pump_count}")
            print()

            print("Filter cycle")
            print("------------")
            print(f"Filter cycle 1 start: {spa.filter_cycle_1_start}")
            print(f"Filter cycle 1 duration: {spa.filter_cycle_1_duration}")
            print(
                f"Filter cycle 2 start: {spa.filter_cycle_2_start} ({'en' if spa.filter_cycle_2_enabled else 'dis'}abled)"
            )
            print(f"Filter cycle 2 duration: {spa.filter_cycle_2_duration}")
            print()

            print("Status update")
            print("-------------")
            print(f"Temperature unit: {spa.temperature_unit.name}")
            print(f"Temperature: {spa.temperature}")
            print(f"Target temperature: {spa.target_temperature}")
            print(f"Temperature range: {spa.temperature_range.state.name}")
            print(f"Heat mode: {spa.heat_mode.state.name}")
            print(f"Heat state: {spa.heat_state.name}")
            print(f"Pump status: {spa.pumps}")
            print(spa.circulation_pump)
            print(f"Light status: {spa.lights}")
            print(f"Mister status: {spa.misters}")
            print(f"Aux status: {spa.aux}")
            print(f"Blower status: {spa.blowers}")
            print(
                f"Spa time: {spa.time_hour:02d}:{spa.time_minute:02d} {'24hr' if spa.is_24_hour else '12hr'}"
            )
            print(f"Filter cycle 1 running: {spa.filter_cycle_1_running}")
            print(f"Filter cycle 2 running: {spa.filter_cycle_2_running}")
            print()

            await test_controls(spa)
    except SpaConnectionError:
        print(f"Failed to connect to spa at {host}")
    else:
        print()
        print(
            "If something is not working as expected, please create an issue and add the above output at:"
        )
        print("https://github.com/garbled1/pybalboa/issues/")
        print()


async def test_controls(spa: SpaClient) -> None:
    """Test spa controls."""
    print("******** Testing spa controls **********")
    print()
    print("Temperature control")
    print("-------------------")
    assert spa.target_temperature is not None
    assert spa.temperature_maximum is not None
    assert spa.temperature_minimum is not None
    target_temperature = spa.target_temperature
    await adjust_temperature(
        spa,
        spa.temperature_maximum
        if spa.target_temperature != spa.temperature_maximum
        else spa.temperature_minimum,
    )
    await adjust_temperature(spa, target_temperature)
    print()

    for control in spa.controls:
        print(f"{control.name} control")
        print("-" * (len(control.name) + 8))
        state = control.state
        for option in control.options:
            if option not in (state, control.state):
                await adjust_control(control, option)
        if control.state != state:
            await adjust_control(control, state)
        print()


async def adjust_temperature(spa: SpaClient, temperature: float) -> None:
    """Adjust target temperature settings."""
    print(f"Current target temperature: {spa.target_temperature}")
    print(f"  Set to {temperature}")
    await spa.set_temperature(temperature)

    async def _temperature_check() -> None:
        while spa.target_temperature != temperature:
            await asyncio.sleep(0.1)

    wait = 10
    try:
        await asyncio.wait_for(_temperature_check(), wait)
        print(f"  Set temperature is now {spa.target_temperature}")
    except asyncio.TimeoutError:
        print(
            f"  Set temperature was not changed after {wait} seconds; is {spa.target_temperature}"
        )


async def adjust_control(control: SpaControl, state: IntEnum) -> None:
    """Adjust control state."""
    print(f"Current state: {control.state.name}")
    print(f"  Set to {state.name}")
    if not await control.set_state(state):
        return

    async def _state_check() -> None:
        while control.state != state:
            await asyncio.sleep(0.1)

    wait = 10
    try:
        await asyncio.wait_for(_state_check(), wait)
        print(f"  State is now {control.state.name}")
    except asyncio.TimeoutError:
        print(f"  State was not changed after {wait} seconds; is {control.state.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a spa and listen for updates.",
        usage=f"{sys.argv[0]} [host] [-d | --debug] [--all]",
    )
    parser.add_argument("host", nargs="?", help="Spa IP address or hostname (optional)")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug logging"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Discover all available spas instead of just the first one.",
    )

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    print(f"pybalboa version: {__version__}")

    if args.host:
        asyncio.run(connect_and_listen(args.host))
    else:
        print("No host provided. Running in discovery mode...")
        asyncio.run(run_discovery(first_spa=not args.all))

    sys.exit(0)
