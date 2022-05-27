import abc
import re
import subprocess
import sys
from typing import Union, Any, Match

from dvpn.config.constants import PublicVars


class VpnCli:
    def __init__(self, cli_path):
        print("\nWelcome to DieVPN\n")
        print(
            "Make sure to kill all VPN clients before usage, as cli would collide with it"
        )
        self.process_pipe = None
        self.cli_path = cli_path

    @abc.abstractmethod
    def get_connected_vpn(self):
        pass

    @classmethod
    @abc.abstractmethod
    def reset(cls, cli_path=None):
        pass

    @abc.abstractmethod
    def __connect(self, host, username, password, **kwargs) -> dict:
        pass

    @abc.abstractmethod
    def connect(self, creds: dict) -> (bool, dict):
        pass

    @classmethod
    def check_containing(
            cls, read_lines: str, searched_list: tuple
    ) -> Union[
        Match[str], None, Match[Union[Union[str, bytes], Any]], tuple[bool, None]
    ]:
        for url in searched_list:
            return re.search(url, read_lines)
        return False, None

    @classmethod
    def dns_records(cls):
        if sys.platform == "win32":
            return subprocess.check_output(["ipconfig", "/displaydns"]).decode()
        elif sys.platform == "darwin":
            return subprocess.check_output(["ipconfig", "/displaydns"]).decode()

    @classmethod
    def flush_dns(cls):
        if sys.platform == "win32":
            return subprocess.check_output(["ipconfig", "/flushdns"]).decode()
        elif sys.platform == "darwin":
            ...

    @classmethod
    def check_accessed(cls):
        out_dict = dict()
        if sys.platform == "win32":
            stdout = cls.dns_records()
            print(stdout)
            credentials = PublicVars().credentials
            for key in credentials.keys():
                out_dict[key] = VpnCli.check_containing(
                    stdout, credentials[key]["urls"]
                )  # Check if A server record error
            print(out_dict)
