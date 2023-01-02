import logging
import os
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
            if vpn_name == info[0]:
                return info[1]
        return None

    def get_connected_vpn(self):
        pass

    def reset(self, cli_path=None, host: str = None):
        print("...Disconnecting")

        os.system(
            f"{self.get_default_cli_path()} launch"
        )

        while host is not None and not (
            "disconnected" in self.get_state(host).lower()
            or "exiting" in self.get_state(host).lower()
        ):
            sleep(0.1)

    def __connect(self, vpn_name) -> dict:
        print(f">> Connecting to {vpn_name}")
        os.system(
            f"{self.get_default_cli_path()} connect {vpn_name}"
        )

        while not (
            "connected" in (state_conn := self.get_state(vpn_name).lower())
            or "disconnected" in state_conn
            or "network_access" in state_conn
            or "exiting" in state_conn
        ):
            sleep(0.1)

        state = self.get_state(vpn_name).lower()
        connected = "connected" in state or "network_access" in state
        return {"connected": connected, "reason": "VPN Error"}

    def connect(self, creds: dict) -> (bool, dict):
        print("~ Resetting connection")
        try:
            self.reset()
        except subprocess.CalledProcessError:
            print("Launching Tunnelblick")
            os.system(
                f"{self.get_default_cli_path()} launch"
            )

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
