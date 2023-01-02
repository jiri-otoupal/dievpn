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


class TunnelblickCLI(VpnCli):
    fields = [
        {"name": "VPN Name", "placeholderText": "Name of VPN configuration"},
    ]
    cli_path_win = "NOT EXISTENT ! MAC OS ONLY"

    cli_path_osx = "tunnelblickctl"

    def get_state(self, vpn_name: str) -> str:
        all_vpns = subprocess.check_output(
            [self.get_default_cli_path(), "status"]
        ).decode()
        for line in all_vpns.split("\n"):
            info = line.split()
            if vpn_name in info[0]:
                return info[1]
        return None

    def get_connected_vpn(self):
        pass

    def reset(self, cli_path=None, vpn_name: str = None):
        print("...Disconnecting")

        subprocess.check_output(
            [self.get_default_cli_path(), "disconnect", "-a"]
        )

        while vpn_name is not None and (
            "disconnected" not in self.get_state(vpn_name).lower()
            or "exiting" not in self.get_state(vpn_name).lower()
        ):
            sleep(0.1)

    def __connect(self, vpn_name) -> dict:
        print(f">> Connecting to {vpn_name}")
        self.output = output = subprocess.check_output(
            [self.get_default_cli_path(), "connect", vpn_name]
        )

        while (
            "connected" not in (state_conn := self.get_state(vpn_name)).lower()
            and "disconnected" not in state_conn.lower()
        ):
            sleep(0.1)

        logging.info("".join(output))
        connected = "connected" in self.get_state(vpn_name).lower()
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
