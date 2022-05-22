import logging
import os
import re
import subprocess
import sys
from typing import Union, Any, Match

from dvpn.config.constants import PublicVars
from dvpn.config.paths import vpn_cli_file_path_win, vpn_cli_file_path_osx

if sys.platform == "win32":
    import wexpect
else:
    import pexpect as wexpect


class VpnCli:
    def __init__(self, cli_path):
        print("\nWelcome to DieVPN\n")
        print(
            "Make sure to kill all VPN clients before usage, as cli would collide with it"
        )
        self.process_pipe = None
        self.cli_path = cli_path
        print("Resetting connection for future stability")
        self.reset()

    def get_connected_vpn(self):
        stdout = subprocess.check_output([self.cli_path, "stats"]).decode()
        # Match and remove dot on end
        vpn_name_index = re.findall(".*onnected to*. .*", stdout)[0][:-1]

        return vpn_name_index.split(" ")[1]

    @classmethod
    def reset(cls, cli_path=None):
        print("...Disconnecting")
        # TODO: fix this for more types of vpn supported
        pipe = wexpect.spawn(
            command=str(vpn_cli_file_path_win)
            if os.name == "nt"
            else str(vpn_cli_file_path_osx),
            args=["disconnect"],
            encoding="utf-8"
        )
        output = pipe.readlines()

        if "disconnected" in "".join(output[-3:-1]).lower():
            print("Disconnected")
        else:
            print("Not Connected")

    def __connect(self, host, username, password, **kwargs):
        print(f">> Connecting to {host}")
        self.process_pipe = wexpect.spawn(
            command=self.cli_path, args=["connect", f"{host}"],
            encoding="utf-8"
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
        return "connected" in "".join(output[-3:-1]).lower()

    def connect(self, creds: dict, banner: bool = False) -> bool:
        print("~ Resetting connection")
        self.reset()
        if self.__connect(**creds):
            print("<Successfully Connected>")
            return True
        else:
            print("Connection failed :(")
            return False

    @classmethod
    def check_containing(
            cls, read_lines: str, searched_list: tuple
    ) -> Union[
        Match[str], None, Match[Union[Union[str, bytes], Any]], tuple[bool, None]
    ]:
        for url in searched_list:
            return re.findall(url, read_lines)
        return False, None

    @classmethod
    def check_accessed(cls):
        out_dict = dict()
        if sys.platform == "win32":
            stdout = subprocess.check_output(["ipconfig", "/displaydns"]).decode()
            print(stdout)
            credentials = PublicVars().credentials
            for key in credentials.keys():
                out_dict[key] = VpnCli.check_containing(
                    stdout, credentials[key]["urls"]
                )  # Check if A server record error
