import logging
import os
from pathlib import Path

import wexpect

vpn_cli_dir_path = r"C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\"

vpn_cli_file_path = Path(f"{vpn_cli_dir_path}\\vpncli{'.exe' if os.name == 'nt' else ''}")


class VpnCli:

    def __init__(self, cli_path):
        print("\nWelcome to DieVPN\n")
        self.process_pipe = None
        self.cli_path = cli_path
        print("Resetting connection for future stability")
        self.reset()

    @classmethod
    def reset(cls, cli_path=None):
        print("...Disconnecting")
        pipe = wexpect.spawn(command=str(vpn_cli_file_path) if cli_path is None else cli_path, args=["disconnect"])
        output = pipe.readlines()

        if "disconnected" in "".join(output[-3:-1]).lower():
            print("Disconnected")
        else:
            print("Not Connected")

    def __connect(self, host, username, password, **kwargs):
        print(f">> Connecting to {host}")
        self.process_pipe = wexpect.spawn(command=self.cli_path, args=["connect", f'{host}'])

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

    def connect(self, creds: dict, banner: bool = False):
        print("~ Resetting connection")
        self.reset()
        if self.__connect(**creds):
            print("<Successfully Connected>")
        else:
            print("Connection failed :(")
