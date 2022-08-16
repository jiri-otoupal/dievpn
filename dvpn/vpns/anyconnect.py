import logging
import os
import re
import subprocess
import sys
from pathlib import Path

from dvpn.vpns.base import VpnCli

if sys.platform == "win32":
    import wexpect
else:
    import pexpect as wexpect


class AnyConnectCLI(VpnCli):
    fields = [
        {"name": "VPN Name", "placeholderText": "My Zoo VPN"},
        {"name": "Host", "placeholderText": "favourite-zoo.com"},
        {"name": "Username", "placeholderText": "giraffe"},
        {"name": "Password", "placeholderText": "******", "sensitive": True},
    ]
    cli_path_win = (
            Path("C:\\")
            / "Program Files (x86)\\"
            / "Cisco\\"
            / "Cisco AnyConnect Secure Mobility Client\\vpncli.exe"
    )

    cli_path_osx = Path("/opt/cisco/anyconnect/bin/vpn")

    def get_state(self, name: str) -> str:
        stdout = subprocess.check_output([self.cli_path, "state", name]).decode()
        # Match and remove dot on end
        vpn_state = re.findall("(.*state:*.) (.*)", stdout)[0][1]

        return vpn_state.replace("\r", "")

    def get_connected_vpn(self):
        stdout = subprocess.check_output([self.cli_path, "stats"]).decode()
        # Match and remove dot on end
        vpn_name_index = re.findall(".*onnected to*. .*", stdout)[0][:-1]

        return vpn_name_index.split(" ")[1]

    def reset(self, cli_path=None, host: str = None):
        print("...Disconnecting")
        arguments = ["disconnect"]

        if host:
            arguments.append(host)

        pipe = wexpect.spawn(
            command=cli_path if cli_path else self.get_default_cli_path(),
            args=arguments,
            encoding="utf-8",
        )
        output = pipe.readlines()

        if "disconnected" in "".join(output[-3:-1]).lower():
            print("Disconnected")
        else:
            print("Not Connected")

    def __connect(self, host, username, password, **kwargs) -> dict:
        print(f">> Connecting to {host}")
        self.process_pipe = wexpect.spawn(
            command=self.cli_path,
            args=["connect", f"{host}"],
            encoding="utf-8",
            timeout=15,
        )

        print("     ... Waiting for VPN to complete its chores")
        self.process_pipe.expect(".*sername*.")
        print("     > Entering Username")
        self.process_pipe.sendline(username)
        self.process_pipe.expect(".*assword*.")
        print("     > Entering Password")
        self.process_pipe.sendline(password)

        if kwargs.get("banner", False):
            self.process_pipe.expect(".*accept*.")
            self.process_pipe.sendline("y")

        output = self.process_pipe.readlines()

        logging.info("".join(output))
        connected = "connected" in "".join(output[-3:-1]).lower()
        return {"connected": connected, "reason": "VPN Error", "log": output}

    def connect(self, creds: dict) -> (bool, dict):
        print("~ Resetting connection")
        self.reset()

        try:
            stat = self.__connect(
                host=creds["Host"],
                username=creds["Username"],
                password=creds["Password"],
                **creds,
            )
        except wexpect.TIMEOUT as ex:
            stat = {"reason": "invalid credentials"}

        if stat.get("connected", False):
            print("<Successfully Connected>")
            return True, stat
        else:
            print("Connection failed :(")
            print(f"Reason {''.join(stat.get('log', ['Unable to read stdout']))}")
            return False, stat
