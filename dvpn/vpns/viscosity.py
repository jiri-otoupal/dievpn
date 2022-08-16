import logging
import subprocess
import sys
from pathlib import Path
from time import sleep

from dvpn.vpns.base import VpnCli

if sys.platform == "win32":
    import wexpect
else:
    import pexpect as wexpect


class ViscosityCLI(VpnCli):
    fields = [
        {"name": "VPN Name", "placeholderText": "Name of VPN in Viscosity"},
    ]
    cli_path_win = Path("C:\\") / "Program Files" / "Viscosity" / "ViscosityCC.exe"

    cli_path_osx = Path("/opt/cisco/anyconnect/bin/vpn")

    def get_state(self, name: str) -> str:
        return subprocess.check_output(
            [
                self.cli_path if self.cli_path else self.get_default_cli_path(),
                "getstate",
                name,
            ]
        ).decode()

    def get_connected_vpn(self):
        pass

    def reset(self, cli_path=None, host: str = None):
        print("...Disconnecting")

        pipe = wexpect.spawn(
            command=cli_path if cli_path else self.get_default_cli_path(),
            args=["disconnect", "all" if host is None else host],
            encoding="utf-8",
        )
        output = pipe.readline()

        while host is not None and "Disconnected" not in self.get_state(host):
            sleep(0.1)

    def __connect(self, host) -> dict:
        print(f">> Connecting to {host}")
        self.process_pipe = wexpect.spawn(
            command=self.cli_path if self.cli_path else self.get_default_cli_path(),
            args=["connect", f"{host}"],
            encoding="utf-8",
            timeout=15,
        )
        output = self.process_pipe.readline()

        while (
            "Connected" not in (state_conn := self.get_state(host))
            and "Disconnected" not in state_conn
        ):
            sleep(0.1)

        logging.info("".join(output))
        connected = "Connected" in self.get_state(host)
        return {"connected": connected, "reason": "VPN Error", "log": output}

    def connect(self, creds: dict) -> (bool, dict):
        print("~ Resetting connection")
        self.reset()

        try:
            stat = self.__connect(creds["VPN Name"])
        except wexpect.TIMEOUT as ex:
            stat = {"reason": "invalid credentials"}

        if stat.get("connected", False):
            print("<Successfully Connected>")
            return True, stat
        else:
            print("Connection failed :(")
            print(f"Reason {''.join(stat.get('log', ['Unable to read stdout']))}")
            return False, stat
